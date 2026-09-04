from __future__ import annotations

import frappe
from frappe.utils import add_days, getdate, nowdate

from it_book.access import require_it_book_access
from it_book.reporting.summary import get_dashboard_summary


@frappe.whitelist()
def dashboard_summary():
    require_it_book_access()
    return get_dashboard_summary()


@frappe.whitelist()
def open_alerts():
    require_it_book_access()
    today = getdate(nowdate())
    return {
        "overdue_projects": frappe.get_all(
            "IT Project",
            filters={"due_date": ["<", today], "status": ["not in", ["Completed", "Cancelled"]]},
            fields=["name", "project_title", "department", "owner_name", "due_date", "alert_status"],
            order_by="due_date asc",
        ),
        "failed_backups": frappe.get_all(
            "IT Backup Log",
            filters={"status": ["in", ["Failed", "Warning"]]},
            fields=["name", "system_name", "backup_date", "status", "remarks"],
            order_by="backup_date desc",
            limit=20,
        ),
        "critical_incidents": frappe.get_all(
            "IT Incident",
            filters={"status": ["not in", ["Closed", "Cancelled"]], "priority": "Critical"},
            fields=["name", "incident_title", "system_name", "reported_on", "status"],
            order_by="reported_on asc",
        ),
        "overdue_asset_returns": frappe.get_all(
            "IT Asset Movement",
            filters={"expected_return_date": ["<", today], "status": ["!=", "Returned"]},
            fields=["name", "asset", "to_person", "department", "expected_return_date", "status"],
            order_by="expected_return_date asc",
        ),
    }


@frappe.whitelist()
def upcoming_due_dates(days: int = 14):
    require_it_book_access()
    today = getdate(nowdate())
    end_date = add_days(today, int(days))
    return {
        "projects": frappe.get_all(
            "IT Project",
            filters={"due_date": ["between", [today, end_date]], "status": ["not in", ["Completed", "Cancelled"]]},
            fields=["name", "project_title", "department", "owner_name", "due_date", "status"],
            order_by="due_date asc",
        ),
        "maintenance": frappe.get_all(
            "IT Maintenance",
            filters={"scheduled_date": ["between", [today, end_date]], "status": ["not in", ["Completed", "Cancelled"]]},
            fields=["name", "maintenance_title", "system_or_asset", "scheduled_date", "status"],
            order_by="scheduled_date asc",
        ),
        "checklists": frappe.get_all(
            "IT Checklist Run",
            filters={"due_date": ["between", [today, end_date]], "status": ["not in", ["Completed", "Cancelled"]]},
            fields=["name", "subject", "person_name", "department", "due_date", "status"],
            order_by="due_date asc",
        ),
    }


@frappe.whitelist()
def recent_activity(limit: int = 20):
    require_it_book_access()
    limit = int(limit)
    return {
        "activities": frappe.get_all(
            "IT Activity Log",
            fields=["name", "activity_title", "activity_type", "system_name", "activity_date", "performed_by"],
            order_by="activity_date desc",
            limit=limit,
        ),
        "incidents": frappe.get_all(
            "IT Incident",
            fields=["name", "incident_title", "system_name", "priority", "status", "reported_on"],
            order_by="reported_on desc",
            limit=limit,
        ),
        "changes": frappe.get_all(
            "IT Change Register",
            fields=["name", "change_title", "change_type", "system_name", "status", "planned_release_date"],
            order_by="modified desc",
            limit=limit,
        ),
    }
