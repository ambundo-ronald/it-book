"""Export likely IT project rows from an Excel workbook to Frappe import CSV.

Usage:
    python it_book/scripts/export_projects_from_xlsx.py "C:/path/NORWA IT PROJECT 2026.xlsx" output/projects.csv

The script uses only Python's standard library so it can run before a bench
environment exists. It extracts rows from the workbook and applies conservative
column mapping heuristics for the current Norwa project dashboard.
"""

from __future__ import annotations

import csv
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

OUTPUT_FIELDS = [
    "project_title",
    "description",
    "owner_name",
    "department",
    "status",
    "priority",
    "planned_budget",
    "actual_spend",
    "start_date",
    "due_date",
    "progress",
    "latest_update",
]

STATUS_WORDS = {
    "planned": "Planned",
    "ongoing": "Ongoing",
    "on testing": "Ongoing",
    "pending review": "Pending Review",
    "pending training": "Ongoing",
    "training conducted": "Pending Review",
    "handed over to user dept": "Completed",
    "completed": "Completed",
    "finished": "Completed",
    "cancelled": "Cancelled",
    "terminated": "Cancelled",
    "at risk": "At Risk",
    "overdue": "At Risk",
    "paused": "At Risk",
    "not started": "Planned",
}


@dataclass
class CandidateProject:
    project_title: str
    description: str = ""
    owner_name: str = ""
    department: str = ""
    status: str = "Planned"
    priority: str = "Medium"
    planned_budget: str = ""
    actual_spend: str = ""
    start_date: str = ""
    due_date: str = ""
    progress: str = ""
    latest_update: str = ""


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip())
        return 2

    workbook = Path(sys.argv[1])
    output = Path(sys.argv[2])
    rows = list(read_workbook_rows(workbook))
    projects = extract_projects(rows)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for project in projects:
            writer.writerow(project.__dict__)

    print(f"Exported {len(projects)} candidate project rows to {output}")
    return 0


def read_workbook_rows(workbook: Path):
    with zipfile.ZipFile(workbook) as package:
        shared_strings = read_shared_strings(package)
        workbook_xml = ET.fromstring(package.read("xl/workbook.xml"))
        rels_xml = ET.fromstring(package.read("xl/_rels/workbook.xml.rels"))
        rel_targets = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels_xml}

        for sheet in workbook_xml.findall("main:sheets/main:sheet", NS):
            rel_id = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
            target = rel_targets[rel_id]
            if not target.startswith("worksheets/"):
                target = f"worksheets/{target}"
            sheet_xml = ET.fromstring(package.read(f"xl/{target}"))
            for row in sheet_xml.findall("main:sheetData/main:row", NS):
                values = []
                for cell in row.findall("main:c", NS):
                    values.append(read_cell_value(cell, shared_strings))
                cleaned = [clean_text(value) for value in values]
                if any(cleaned):
                    yield cleaned


def read_shared_strings(package: zipfile.ZipFile) -> list[str]:
    try:
        xml = ET.fromstring(package.read("xl/sharedStrings.xml"))
    except KeyError:
        return []

    strings = []
    for item in xml.findall("main:si", NS):
        parts = [node.text or "" for node in item.findall(".//main:t", NS)]
        strings.append("".join(parts))
    return strings


def read_cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    value = cell.findtext("main:v", default="", namespaces=NS)
    if cell.attrib.get("t") == "s" and value:
        return shared_strings[int(value)]
    return value


def extract_projects(rows: list[list[str]]) -> list[CandidateProject]:
    projects: list[CandidateProject] = []

    for row in rows:
        cells = [cell for cell in row if cell]
        if len(cells) < 3:
            continue
        if is_dashboard_noise(cells):
            continue

        structured_project = extract_structured_project(cells)
        if structured_project:
            projects.append(structured_project)

    return deduplicate(projects)


def is_dashboard_noise(cells: list[str]) -> bool:
    joined = " ".join(cells).lower()
    noise = [
        "norwa it project dashboard",
        "date of last update",
        "portfolio progress",
        "portfolio financial health",
        "total planned budget",
        "budget utilization rate",
        "department lead",
        "expected date of completion",
        "deliverables by priority",
        "automation by status",
    ]
    return any(term in joined for term in noise)


def extract_structured_project(cells: list[str]) -> CandidateProject | None:
    if len(cells) < 7:
        return None
    if not normalize_status(cells[5]):
        return None
    if cells[4] not in {"Low", "Medium", "High", "Extreme", "Critical"}:
        return None

    return CandidateProject(
        department=cells[0],
        project_title=cells[2],
        description=cells[3],
        priority=normalize_priority(cells[4]),
        status=normalize_status(cells[5]) or "Planned",
        owner_name=cells[6] if len(cells) > 6 and not looks_numeric(cells[6]) else "",
        planned_budget=clean_number(cells[7]) if len(cells) > 7 else "",
        actual_spend=clean_number(cells[8]) if len(cells) > 8 else "",
        start_date=excel_date_to_iso(cells[10]) if len(cells) > 10 else "",
        due_date=excel_date_to_iso(cells[11]) if len(cells) > 11 else "",
        progress=excel_progress(cells[14]) if len(cells) > 14 else "",
        latest_update=" | ".join(cells),
    )


def find_project_title(cells: list[str]) -> str:
    candidates = [
        cell
        for cell in cells
        if len(cell) > 3
        and not looks_numeric(cell)
        and normalize_status(cell) == ""
        and cell.lower() not in {"department", "status", "description"}
    ]
    if not candidates:
        return ""
    return max(candidates, key=len)[:140]


def find_status(cells: list[str]) -> str:
    for cell in cells:
        status = normalize_status(cell)
        if status:
            return status
    return "Planned"


def find_priority(cells: list[str]) -> str:
    for cell in cells:
        priority = normalize_priority(cell)
        if priority:
            return priority
    return "Medium"


def normalize_priority(value: str) -> str:
    priorities = {
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "extreme": "Critical",
        "critical": "Critical",
    }
    return priorities.get(value.strip().lower(), "")


def find_department(cells: list[str]) -> str:
    known_departments = {
        "ict",
        "finance",
        "operations",
        "sales",
        "procurement",
        "logistics",
        "engineering",
        "hr",
    }
    for cell in cells:
        if cell.lower() in known_departments:
            return cell
    return ""


def find_owner(cells: list[str], project_title: str, status: str, department: str) -> str:
    for cell in cells:
        if cell in {project_title, status, department}:
            continue
        if looks_person_name(cell):
            return cell
    return ""


def find_description(cells: list[str], project_title: str) -> str:
    for cell in cells:
        if cell != project_title and len(cell) > 20 and not looks_numeric(cell):
            return cell
    return ""


def normalize_status(value: str) -> str:
    return STATUS_WORDS.get(value.strip().lower(), "")


def looks_person_name(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][A-Za-z.'-]{2,}( [A-Z][A-Za-z.'-]{2,})?", value.strip()))


def looks_numeric(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


def clean_number(value: str) -> str:
    if value in {"", "-", "–"}:
        return ""
    return value


def excel_progress(value: str) -> str:
    if not looks_numeric(value):
        return ""
    number = float(value)
    if 0 <= number <= 1:
        number *= 100
    return str(round(number, 2))


def excel_date_to_iso(value: str) -> str:
    if not looks_numeric(value):
        return ""
    serial = int(float(value))
    if serial < 30000:
        return ""

    from datetime import date, timedelta

    # Excel's Windows date system stores 1900-01-01 as 1 and includes the
    # historical leap-year bug, so 1899-12-30 is the practical epoch.
    return (date(1899, 12, 30) + timedelta(days=serial)).isoformat()


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def deduplicate(projects: list[CandidateProject]) -> list[CandidateProject]:
    seen = set()
    unique = []
    for project in projects:
        key = project.project_title.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(project)
    return unique


if __name__ == "__main__":
    raise SystemExit(main())
