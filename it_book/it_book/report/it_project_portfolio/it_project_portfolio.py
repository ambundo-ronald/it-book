from __future__ import annotations

import frappe


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Project", "fieldname": "project_title", "fieldtype": "Data", "width": 240},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 130},
        {"label": "Owner", "fieldname": "owner_name", "fieldtype": "Data", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 110},
        {"label": "Progress", "fieldname": "progress", "fieldtype": "Percent", "width": 100},
        {"label": "Planned Budget", "fieldname": "planned_budget", "fieldtype": "Currency", "width": 140},
        {"label": "Actual Spend", "fieldname": "actual_spend", "fieldtype": "Currency", "width": 140},
        {"label": "Budget Use", "fieldname": "budget_utilization", "fieldtype": "Percent", "width": 110},
        {"label": "Alert", "fieldname": "alert_status", "fieldtype": "Data", "width": 140},
    ]


def get_data(filters):
    query_filters = {}
    if filters.get("department"):
        query_filters["department"] = filters["department"]
    if filters.get("status"):
        query_filters["status"] = filters["status"]

    return frappe.get_all(
        "IT Project",
        filters=query_filters,
        fields=[
            "project_title",
            "department",
            "owner_name",
            "status",
            "priority",
            "due_date",
            "progress",
            "planned_budget",
            "actual_spend",
            "budget_utilization",
            "alert_status",
        ],
        order_by="due_date asc, modified desc",
    )
