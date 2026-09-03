from __future__ import annotations

import frappe


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


def get_columns():
    return [
        {"label": "Incident", "fieldname": "incident_title", "fieldtype": "Data", "width": 240},
        {"label": "System", "fieldname": "system_name", "fieldtype": "Data", "width": 150},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 130},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
        {"label": "Incident Status", "fieldname": "incident_status", "fieldtype": "Data", "width": 130},
        {"label": "Reported On", "fieldname": "reported_on", "fieldtype": "Datetime", "width": 170},
        {"label": "Downtime Start", "fieldname": "start_time", "fieldtype": "Datetime", "width": 170},
        {"label": "Downtime End", "fieldname": "end_time", "fieldtype": "Datetime", "width": 170},
        {"label": "Minutes", "fieldname": "duration_minutes", "fieldtype": "Float", "width": 90},
        {"label": "Business Impact", "fieldname": "business_impact", "fieldtype": "Data", "width": 130},
    ]


def get_data(filters):
    conditions = []
    values = {}
    if filters.get("priority"):
        conditions.append("incident.priority = %(priority)s")
        values["priority"] = filters["priority"]
    if filters.get("status"):
        conditions.append("incident.status = %(status)s")
        values["status"] = filters["status"]

    where_clause = f"where {' and '.join(conditions)}" if conditions else ""
    return frappe.db.sql(
        f"""
        select
            incident.incident_title,
            incident.system_name,
            incident.department,
            incident.priority,
            incident.status as incident_status,
            incident.reported_on,
            downtime.start_time,
            downtime.end_time,
            downtime.duration_minutes,
            downtime.business_impact
        from `tabIT Incident` incident
        left join `tabIT Downtime` downtime on downtime.incident = incident.name
        {where_clause}
        order by incident.reported_on desc
        """,
        values,
        as_dict=True,
    )
