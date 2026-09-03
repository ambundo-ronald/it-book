from __future__ import annotations

import frappe
from frappe.utils import add_days, flt, getdate, nowdate


def get_dashboard_summary() -> dict:
    today = getdate(nowdate())
    open_project_statuses = ["Planned", "Ongoing", "Pending Review", "At Risk"]

    projects = frappe.get_all(
        "IT Project",
        fields=["name", "status", "progress", "planned_budget", "actual_spend", "due_date"],
    )
    incidents = frappe.get_all("IT Incident", filters={"status": ["!=", "Closed"]}, fields=["name", "priority"])
    downtime = frappe.get_all("IT Downtime", filters={"status": ["not in", ["Resolved", "Closed"]]}, fields=["name", "duration_minutes"])
    backups = frappe.get_all("IT Backup Log", filters={"backup_date": [">=", add_days(today, -7)]}, fields=["name", "status"])
    assets_due = frappe.db.count("IT Asset Movement", {"expected_return_date": ["<", today], "status": ["!=", "Returned"]})

    open_projects = [p for p in projects if p.status in open_project_statuses]
    failed_backups = [b for b in backups if b.status in ("Failed", "Warning")]

    return {
        "projects_total": len(projects),
        "projects_open": len(open_projects),
        "projects_at_risk": len([p for p in projects if p.status == "At Risk"]),
        "average_progress": _average([p.progress for p in projects]),
        "planned_budget": sum(flt(p.planned_budget) for p in projects),
        "actual_spend": sum(flt(p.actual_spend) for p in projects),
        "open_incidents": len(incidents),
        "critical_incidents": len([i for i in incidents if i.priority == "Critical"]),
        "active_downtime_events": len(downtime),
        "downtime_minutes_open": sum(flt(d.duration_minutes) for d in downtime),
        "backup_checks_7d": len(backups),
        "backup_warnings_7d": len(failed_backups),
        "overdue_asset_returns": assets_due,
        "budget_utilization": _budget_utilization(projects),
    }


def send_daily_summary():
    _send_summary("Daily IT Book Summary", "Daily")


def send_weekly_summary():
    _send_summary("Weekly IT Book Summary", "Weekly")


def flag_overdue_and_unrealistic_records():
    today = getdate(nowdate())

    for project in frappe.get_all(
        "IT Project",
        filters={"due_date": ["<", today], "status": ["not in", ["Completed", "Cancelled"]]},
        fields=["name"],
    ):
        frappe.db.set_value("IT Project", project.name, "alert_status", "Overdue")

    for project in frappe.get_all(
        "IT Project",
        filters={"progress": [">", 100]},
        fields=["name"],
    ):
        frappe.db.set_value("IT Project", project.name, "alert_status", "Unrealistic Report")

    for log in frappe.get_all(
        "IT Backup Log",
        filters={"status": ["in", ["Failed", "Warning"]], "backup_date": [">=", add_days(today, -1)]},
        fields=["name"],
    ):
        frappe.db.set_value("IT Backup Log", log.name, "requires_attention", 1)


def _send_summary(subject: str, frequency: str):
    recipients = [
        row.email
        for row in frappe.get_all(
            "IT Report Recipient",
            filters={"enabled": 1, "frequency": ["in", [frequency, "Both"]]},
            fields=["email"],
        )
    ]
    if not recipients:
        return

    summary = get_dashboard_summary()
    alerts = _get_email_alert_rows()
    message = frappe.render_template(
        """
        <h3>{{ subject }}</h3>
        <ul>
          <li>Open projects: {{ summary.projects_open }} / {{ summary.projects_total }}</li>
          <li>Projects at risk: {{ summary.projects_at_risk }}</li>
          <li>Average progress: {{ summary.average_progress }}%</li>
          <li>Budget: {{ summary.actual_spend }} actual / {{ summary.planned_budget }} planned</li>
          <li>Open incidents: {{ summary.open_incidents }} (critical: {{ summary.critical_incidents }})</li>
          <li>Active downtime events: {{ summary.active_downtime_events }}</li>
          <li>Backup warnings in last 7 days: {{ summary.backup_warnings_7d }}</li>
          <li>Overdue asset returns: {{ summary.overdue_asset_returns }}</li>
        </ul>
        {% if alerts %}
        <h4>Open Alerts</h4>
        <table border="1" cellspacing="0" cellpadding="4">
          <thead>
            <tr>
              <th>Type</th>
              <th>Reference</th>
              <th>Detail</th>
              <th>Due / Date</th>
            </tr>
          </thead>
          <tbody>
          {% for alert in alerts %}
            <tr>
              <td>{{ alert.type }}</td>
              <td>{{ alert.reference }}</td>
              <td>{{ alert.detail }}</td>
              <td>{{ alert.date or "" }}</td>
            </tr>
          {% endfor %}
          </tbody>
        </table>
        {% endif %}
        """,
        {"subject": subject, "summary": summary, "alerts": alerts},
    )
    frappe.sendmail(recipients=recipients, subject=subject, message=message)


def _average(values) -> float:
    clean_values = [flt(v) for v in values if v is not None]
    if not clean_values:
        return 0
    return round(sum(clean_values) / len(clean_values), 2)


def _budget_utilization(projects) -> float:
    planned = sum(flt(p.planned_budget) for p in projects)
    actual = sum(flt(p.actual_spend) for p in projects)
    if not planned:
        return 0
    return round(actual / planned * 100, 2)


def _get_email_alert_rows() -> list[dict]:
    today = getdate(nowdate())
    rows = []

    for project in frappe.get_all(
        "IT Project",
        filters={"due_date": ["<", today], "status": ["not in", ["Completed", "Cancelled"]]},
        fields=["name", "project_title", "department", "due_date"],
        order_by="due_date asc",
        limit=10,
    ):
        rows.append(
            {
                "type": "Overdue Project",
                "reference": project.name,
                "detail": f"{project.project_title} ({project.department or 'No department'})",
                "date": project.due_date,
            }
        )

    for backup in frappe.get_all(
        "IT Backup Log",
        filters={"status": ["in", ["Failed", "Warning"]]},
        fields=["name", "system_name", "status", "backup_date"],
        order_by="backup_date desc",
        limit=10,
    ):
        rows.append(
            {
                "type": "Backup",
                "reference": backup.name,
                "detail": f"{backup.system_name}: {backup.status}",
                "date": backup.backup_date,
            }
        )

    for incident in frappe.get_all(
        "IT Incident",
        filters={"priority": "Critical", "status": ["not in", ["Closed", "Cancelled"]]},
        fields=["name", "incident_title", "system_name", "reported_on"],
        order_by="reported_on asc",
        limit=10,
    ):
        rows.append(
            {
                "type": "Critical Incident",
                "reference": incident.name,
                "detail": f"{incident.incident_title} ({incident.system_name or 'No system'})",
                "date": incident.reported_on,
            }
        )

    return rows[:20]
