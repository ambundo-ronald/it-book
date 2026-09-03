# IT Book Blueprint

## Product Goal

IT Book is a live IT department operations register. It should replace scattered spreadsheets with a Frappe app that records work, summarizes health, flags risks, and sends scheduled reports.

## Existing Spreadsheet Seed

The workbook `NORWA IT PROJECT 2026.xlsx` contains a project dashboard for 2026. It includes:

- IT project portfolio progress
- Department and owner tracking
- Status values such as pending review, training conducted, testing, and handover
- Planned budget, actual spend, and utilization
- Department groupings like ICT, Finance, Operations, Sales, Procurement, and Logistics

These map into `IT Project` fields:

- Project name -> `project_title`
- Department -> `department`
- Lead or assignee -> `owner_name`
- Status -> `status`
- Budget -> `planned_budget`
- Spend -> `actual_spend`
- Completion/progress -> `progress`
- Latest notes -> `latest_update`

## Frappe Modules

### Project Portfolio

DocType: `IT Project`

Tracks projects being undertaken by IT, including owner, department, due date, progress, budget, actual spend, status, and alert status. This is the source for portfolio dashboard cards and project summary reports.

### Maintenance

DocType: `IT Maintenance`

Tracks preventive, corrective, emergency, and inspection maintenance. Supports scheduled date, completion date, system or asset, findings, next due date, and responsible person.

### Checklists

DocTypes:

- `IT Checklist Template`
- `IT Checklist Template Item`
- `IT Checklist Run`
- `IT Checklist Run Item`

Use templates for onboarding, offboarding, audit, backup, asset handover, and maintenance checklists. A run is created for a specific staff member, asset, department, or operational event.

### Assets

DocTypes:

- `IT Asset Record`
- `IT Asset Movement`

Tracks asset acknowledgement, assignment, repair, return, transfer, disposal, and lifecycle condition. `IT Asset Movement` keeps the audit trail.

### Operations Reporting

DocTypes:

- `IT Backup Log`
- `IT Activity Log`
- `IT Incident`
- `IT Downtime`

These cover backup health, activity reports, system usage, user administration activity, downtime reports, and incident management.

### Change Management

DocType: `IT Change Register`

Tracks new features, enhancements, discontinued features, emergency changes, risk, approval status, release notes, and rollback plans.

### Report Distribution

DocType: `IT Report Recipient`

Stores recipients for daily, weekly, or both summary emails. Scheduled jobs in `it_book.reporting.summary` send the summaries.

## Live Dashboard Summary

The first dashboard should show:

- Total projects
- Open projects
- Projects at risk
- Average progress
- Planned budget vs actual spend
- Open incidents
- Critical incidents
- Active downtime events
- Downtime minutes open
- Backup warnings in the last 7 days
- Overdue asset returns

The backend function is `it_book.reporting.summary.get_dashboard_summary`.

The scaffold includes a Frappe Desk page at `it-book-dashboard`, linked as `Live Dashboard` from the IT Book workspace.

Whitelisted report endpoints:

- `it_book.reporting.api.dashboard_summary`
- `it_book.reporting.api.open_alerts`
- `it_book.reporting.api.upcoming_due_dates`
- `it_book.reporting.api.recent_activity`

## Alerts

Initial automated alerts:

- Project due date has passed while not completed or cancelled -> `Overdue`
- Project progress is above 100 -> `Unrealistic Report`
- Backup status is failed or warning in the last day -> `requires_attention`
- Asset movement expected return date passed while not returned -> dashboard warning
- High or critical risk changes require rollback plans before approval/release
- Released changes require release notes
- Downtime duration is calculated from start and end time

Recommended next alerts:

- Budget utilization above 100%
- Critical incident open for more than 4 hours
- Backup not submitted for a critical system within 24 hours
- Change released without rollback plan
- Asset warranty expiring in the next 30 days

## Workflows To Add In Frappe

### IT Project

Planned -> Ongoing -> Pending Review -> Completed

Risk branches:

- Ongoing -> At Risk
- At Risk -> Ongoing
- Any active state -> Cancelled

### IT Asset Movement

Open -> Approved -> Closed

Disposal should require IT Manager approval and an attachment.

`IT Asset Movement` is submittable. On submit it updates the linked asset status and assignment details.

### IT Change Register

Requested -> Impact Review -> Approved -> In Progress -> Released

Alternative endings:

- Rejected
- Rolled Back
- Discontinued

## Roles

- `IT Manager`: full control of IT Book records and reporting setup
- `IT Officer`: create and update operational records
- `Department Head`: view department-facing records and create incidents
- `IT Auditor`: read-only access for audit and compliance

## Import Plan

1. Clean the project spreadsheet so each project row has one project title, department, owner, status, progress, budget, and latest update.
2. Export the cleaned sheet as CSV.
3. Use Frappe Data Import Tool against `IT Project`.
4. Normalize statuses to the values in the DocType.
5. Review budget and progress fields for unrealistic values.

Generate a candidate CSV locally at `output/it_project_import_candidates.csv` using `it_book/scripts/export_projects_from_xlsx.py`.

## MVP Build Order

1. Install the app in a development bench.
2. Run `bench migrate`.
3. Create roles and assign IT users.
4. Create sample checklist templates.
5. Import the spreadsheet project portfolio.
6. Build a workspace/dashboard page around `get_dashboard_summary`.
7. Configure Email Account and create `IT Report Recipient` records.
8. Add workflows and notification rules.

The scaffold includes starter Workspace, Number Card, and Dashboard Chart fixture JSON files. A live bench may still need these fixtures exported again after the UI is adjusted in Desk.

## Standard Reports

The app includes starter Script Reports for:

- IT Project Portfolio
- IT Backup Health
- IT Incident Downtime
- IT Asset Register
- IT Change Register Report

These reports have lightweight Desk filters and are linked from the IT Book workspace.
