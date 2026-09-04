# IT Book

IT Book is a Frappe app blueprint for an IT department operating register. It tracks IT projects, maintenance, onboarding/offboarding checklists, system usage activities, asset acknowledgement and lifecycle events, backup logs, incidents, downtime, and change management.

The current workspace contains a starter custom app scaffold and implementation notes. The source spreadsheet `NORWA IT PROJECT 2026.xlsx` was used as the seed for the project portfolio model, including status, department, owner, budget, spend, and progress reporting.

## Core Modules

- IT Projects and portfolio reporting
- Preventive and corrective maintenance records
- Onboarding, offboarding, audit, and recurring operational checklists
- Asset acknowledgement, assignment, repair, disposal, and movement history
- Backup logs and backup health reporting
- Activity, system usage, incident, and downtime reports
- Change management register for new, changed, and discontinued features
- Daily and weekly summary emails
- Due date alerts and report anomaly flags

## Frappe Cloud Install

Use repository `https://github.com/ambundo-ronald/it-book` and branch `master`. The Frappe app root is `it_book/`, with `pyproject.toml` at `it_book/pyproject.toml` and hooks at `it_book/hooks.py`.

## Install In A Frappe Bench

From a machine with Frappe Bench installed:

```bash
cd /path/to/frappe-bench/apps
cp -R "/path/to/IT Book/it_book" .
cd /path/to/frappe-bench
bench --site your-site.local install-app it_book
bench --site your-site.local migrate
bench --site your-site.local clear-cache
```

For development, a cleaner path is to create a bench app with `bench new-app it_book`, then copy the files from this scaffold over the generated app package.

## Useful Entry Points

- App hooks: `it_book/hooks.py`
- Dashboard and email summary logic: `it_book/reporting/summary.py`
- Whitelisted dashboard/report APIs: `it_book/reporting/api.py`
- Blueprint: `docs/it-book-blueprint.md`
- Doctype catalog: `docs/frappe-doctype-catalog.md`
- Spreadsheet import helper: `it_book/scripts/export_projects_from_xlsx.py`
- Generated project import CSV: create locally under `output/`

## Next Build Steps

1. Generate these DocTypes inside a live Frappe bench so Frappe can create the database tables and standard metadata.
2. Build dashboard pages using the summary service in `it_book.reporting.summary`.
3. Add role permissions for System Manager, IT Manager, IT Officer, and IT Auditor.
4. Import the existing spreadsheet rows into `IT Project`.
5. Add workflow states for approval-heavy records like disposal, change management, and incident closure.

## Import Current Project Spreadsheet

Generate a candidate import file locally:

```bash
python it_book/scripts/export_projects_from_xlsx.py "C:/Users/Norwa Africa/Downloads/NORWA IT PROJECT 2026.xlsx" output/it_project_import_candidates.csv
```

Review `output/it_project_import_candidates.csv`, then import it into the `IT Project` DocType with Frappe's Data Import Tool.

## Desk Setup After Install

1. Open the `IT Book` workspace.
2. Open `Live Dashboard` for the live IT summary page.
3. Confirm the seeded checklist templates exist.
4. Create at least one `IT Report Recipient`.
5. Configure an outgoing Email Account in Frappe.
6. Import `output/it_project_import_candidates.csv` into `IT Project`.
7. Use the scheduled jobs in `hooks.py` for daily and weekly summary emails.

## Access Control

IT Book is hidden from users unless they have `System Manager`, `IT Manager`, `IT Officer`, or `IT Auditor`. The Desk module icon, workspace, dashboard page, reports, and dashboard APIs are restricted to those roles.

## Included Reports

- `IT Project Portfolio`
- `IT Backup Health`
- `IT Incident Downtime`
- `IT Asset Register`
- `IT Change Register Report`

## Local Scaffold Validation

Without a Frappe bench, you can still validate the scaffold files:

```bash
python it_book/scripts/validate_scaffold.py
```
