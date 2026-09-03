from __future__ import annotations

import frappe
from frappe.utils import add_days, getdate, nowdate


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


def get_columns():
    return [
        {"label": "System", "fieldname": "system_name", "fieldtype": "Data", "width": 180},
        {"label": "Backup Type", "fieldname": "backup_type", "fieldtype": "Data", "width": 120},
        {"label": "Backup Date", "fieldname": "backup_date", "fieldtype": "Datetime", "width": 170},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Size GB", "fieldname": "size_gb", "fieldtype": "Float", "width": 90},
        {"label": "Restore Verified", "fieldname": "verified_restore", "fieldtype": "Check", "width": 120},
        {"label": "Attention", "fieldname": "requires_attention", "fieldtype": "Check", "width": 90},
        {"label": "Location", "fieldname": "storage_location", "fieldtype": "Data", "width": 180},
        {"label": "Remarks", "fieldname": "remarks", "fieldtype": "Small Text", "width": 260},
    ]


def get_data(filters):
    query_filters = {}
    if filters.get("status"):
        query_filters["status"] = filters["status"]
    if filters.get("days"):
        query_filters["backup_date"] = [">=", add_days(getdate(nowdate()), -int(filters["days"]))]

    return frappe.get_all(
        "IT Backup Log",
        filters=query_filters,
        fields=[
            "system_name",
            "backup_type",
            "backup_date",
            "status",
            "size_gb",
            "verified_restore",
            "requires_attention",
            "storage_location",
            "remarks",
        ],
        order_by="backup_date desc",
    )
