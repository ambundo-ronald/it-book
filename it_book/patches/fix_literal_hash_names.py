from __future__ import annotations

import frappe
from frappe.model.naming import make_autoname


LITERAL_HASH_NAMES = {
    "IT Project": "IT-PROJ-#####",
    "IT Maintenance": "IT-MAINT-#####",
    "IT Checklist Run": "IT-CHK-#####",
    "IT Asset Record": "IT-ASSET-#####",
    "IT Asset Movement": "IT-ASSET-MOVE-#####",
    "IT Backup Log": "IT-BACKUP-#####",
    "IT Activity Log": "IT-ACT-#####",
    "IT Incident": "IT-INC-#####",
    "IT Downtime": "IT-DOWN-#####",
    "IT Change Register": "IT-CHG-#####",
}


def execute():
    for doctype, bad_name in LITERAL_HASH_NAMES.items():
        if not frappe.db.exists(doctype, bad_name):
            continue

        prefix = bad_name.replace("#####", "LEGACY")
        new_name = make_autoname(f"{prefix}-.#####")
        frappe.rename_doc(doctype, bad_name, new_name, force=True, ignore_permissions=True)