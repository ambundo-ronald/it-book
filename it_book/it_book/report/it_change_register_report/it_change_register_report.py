from __future__ import annotations

import frappe


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


def get_columns():
    return [
        {"label": "Change", "fieldname": "change_title", "fieldtype": "Data", "width": 240},
        {"label": "Type", "fieldname": "change_type", "fieldtype": "Data", "width": 150},
        {"label": "System", "fieldname": "system_name", "fieldtype": "Data", "width": 150},
        {"label": "Requested By", "fieldname": "requested_by", "fieldtype": "Data", "width": 130},
        {"label": "Owner", "fieldname": "owner_name", "fieldtype": "Data", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
        {"label": "Risk", "fieldname": "risk_level", "fieldtype": "Data", "width": 100},
        {"label": "Requested Date", "fieldname": "requested_date", "fieldtype": "Date", "width": 120},
        {"label": "Release Date", "fieldname": "planned_release_date", "fieldtype": "Date", "width": 120},
    ]


def get_data(filters):
    query_filters = {}
    if filters.get("status"):
        query_filters["status"] = filters["status"]
    if filters.get("change_type"):
        query_filters["change_type"] = filters["change_type"]

    return frappe.get_all(
        "IT Change Register",
        filters=query_filters,
        fields=[
            "change_title",
            "change_type",
            "system_name",
            "requested_by",
            "owner_name",
            "status",
            "risk_level",
            "requested_date",
            "planned_release_date",
        ],
        order_by="planned_release_date asc, modified desc",
    )
