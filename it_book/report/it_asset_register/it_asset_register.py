from __future__ import annotations

import frappe


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


def get_columns():
    return [
        {"label": "Asset", "fieldname": "asset_name", "fieldtype": "Data", "width": 220},
        {"label": "Asset Tag", "fieldname": "asset_tag", "fieldtype": "Data", "width": 130},
        {"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 130},
        {"label": "Serial Number", "fieldname": "serial_number", "fieldtype": "Data", "width": 150},
        {"label": "Assigned To", "fieldname": "assigned_to", "fieldtype": "Data", "width": 150},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
        {"label": "Condition", "fieldname": "condition", "fieldtype": "Data", "width": 110},
        {"label": "Warranty Expiry", "fieldname": "warranty_expiry", "fieldtype": "Date", "width": 120},
    ]


def get_data(filters):
    query_filters = {}
    if filters.get("status"):
        query_filters["status"] = filters["status"]
    if filters.get("department"):
        query_filters["department"] = filters["department"]

    return frappe.get_all(
        "IT Asset Record",
        filters=query_filters,
        fields=[
            "asset_name",
            "asset_tag",
            "category",
            "serial_number",
            "assigned_to",
            "department",
            "status",
            "condition",
            "warranty_expiry",
        ],
        order_by="status asc, asset_name asc",
    )
