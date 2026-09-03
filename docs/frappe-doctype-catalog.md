# Frappe DocType Catalog

## IT Project

Purpose: Track project work being undertaken by IT.

Key fields: project title, department, owner, status, priority, dates, progress, planned budget, actual spend, budget utilization, alert status, description, latest update.

Reports:

- Project portfolio by department
- Projects at risk
- Budget utilization
- Overdue projects

## IT Maintenance

Purpose: Track maintenance performed on systems and assets.

Key fields: maintenance title, type, system or asset, scheduled date, completed date, status, performed by, findings, next due date.

Reports:

- Maintenance completed this week
- Upcoming maintenance
- Deferred maintenance

## IT Checklist Template

Purpose: Store reusable onboarding, offboarding, maintenance, audit, backup, and handover checklist templates.

Child table: `IT Checklist Template Item`.

## IT Checklist Run

Purpose: Track completion of a checklist for a specific person, department, asset, or event.

Child table: `IT Checklist Run Item`.

Reports:

- Open onboarding checklists
- Open offboarding checklists
- Overdue checklist items

## IT Asset Record

Purpose: Track IT assets and current assignment state.

Key fields: asset name, asset tag, category, serial number, assigned to, department, status, purchase date, warranty expiry, condition, acknowledgement file.

Reports:

- Assigned assets
- Assets under repair
- Assets due for disposal
- Warranty expiry

## IT Asset Movement

Purpose: Track asset acknowledgement, assignments, returns, repairs, transfers, and disposal.

Key fields: asset, movement type, from, to, department, movement date, expected return date, status, approval reference, attachment.

Reports:

- Overdue returns
- Repair history
- Disposal register
- Asset assignment history

## IT Backup Log

Purpose: Track backups and restore verification.

Key fields: system, backup type, backup date, status, size, storage location, restore verified, requires attention, remarks.

Reports:

- Backup failures
- Backup warnings
- Restore verification gaps

## IT Activity Log

Purpose: Track support, system usage, administration, security, training, and audit activities.

Key fields: activity title, type, system, department, activity date, performed by, impact, details.

Reports:

- Activity by system
- Activity by department
- Security activity report

## IT Incident

Purpose: Track incidents from report to closure.

Key fields: incident title, reported on, reported by, system, department, priority, status, root cause, resolution, closed on.

Reports:

- Open incidents
- Critical incidents
- Incident root causes
- Resolution performance

## IT Downtime

Purpose: Track service downtime and impact.

Key fields: system, incident, start time, end time, duration, affected users, business impact, status, notes.

Reports:

- Downtime by system
- Downtime minutes by month
- Critical downtime events

## IT Change Register

Purpose: Track new features, changed features, discontinued features, infrastructure changes, security changes, and emergency changes.

Key fields: change title, change type, system, requested by, owner, dates, status, risk level, approval notes, rollback plan, release notes.

Reports:

- Upcoming releases
- Pending approvals
- Discontinued features
- Rolled back changes

## IT Report Recipient

Purpose: Configure scheduled email recipients.

Key fields: email, recipient name, frequency, enabled.

## Standard Reports

The scaffold includes these Script Reports:

- `IT Project Portfolio`: project health, progress, budget, and alert status
- `IT Backup Health`: backup results, restore verification, and attention flags
- `IT Incident Downtime`: incident records joined with downtime impact
- `IT Asset Register`: asset assignment, condition, status, and warranty view
- `IT Change Register Report`: changes by type, owner, status, risk, and release date
