from __future__ import annotations

import frappe


def create_default_records():
    create_checklist_templates()


def create_checklist_templates():
    templates = {
        "Employee Onboarding Checklist": {
            "checklist_type": "Onboarding",
            "items": [
                "Create ERPNext user account",
                "Create email account",
                "Assign laptop or desktop",
                "Issue asset acknowledgement form",
                "Grant department system permissions",
                "Enroll user in MFA where applicable",
                "Conduct IT orientation",
            ],
        },
        "Employee Offboarding Checklist": {
            "checklist_type": "Offboarding",
            "items": [
                "Disable ERPNext user account",
                "Disable email account or delegate mailbox",
                "Recover laptop, phone, and peripherals",
                "Revoke VPN and remote access",
                "Transfer ownership of shared files",
                "Confirm asset return condition",
                "Archive offboarding evidence",
            ],
        },
        "Weekly Backup Verification": {
            "checklist_type": "Backup",
            "items": [
                "Confirm scheduled backups completed",
                "Review failed or warning backup jobs",
                "Verify offsite backup availability",
                "Run restore test for selected system",
                "Record backup size and storage location",
            ],
        },
        "Asset Handover Checklist": {
            "checklist_type": "Asset Handover",
            "items": [
                "Confirm serial number and asset tag",
                "Record physical condition",
                "Attach signed acknowledgement",
                "Assign asset to user and department",
                "Record expected return date if temporary",
            ],
        },
    }

    for template_name, payload in templates.items():
        if frappe.db.exists("IT Checklist Template", template_name):
            continue

        doc = frappe.new_doc("IT Checklist Template")
        doc.template_name = template_name
        doc.checklist_type = payload["checklist_type"]
        for item in payload["items"]:
            doc.append("items", {"task": item, "is_mandatory": 1})
        doc.insert(ignore_permissions=True)
