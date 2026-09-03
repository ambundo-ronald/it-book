import frappe
from frappe.model.document import Document


class ITAssetMovement(Document):
    def validate(self):
        if self.movement_type == "Disposal" and self.status == "Approved" and not self.attachment:
            frappe.throw("Attach disposal approval evidence before approving disposal.")

        if self.movement_type in ("Assignment", "Transfer") and not self.to_person:
            frappe.throw("To is required for asset assignment or transfer.")

    def on_submit(self):
        self.update_asset_status()

    def update_asset_status(self):
        status_by_movement = {
            "Assignment": "Assigned",
            "Return": "Available",
            "Repair": "Under Repair",
            "Disposal": "Disposed",
            "Transfer": "Assigned",
        }
        asset_status = status_by_movement.get(self.movement_type)
        if not asset_status:
            return

        values = {"status": asset_status}
        if self.movement_type in ("Assignment", "Transfer"):
            values.update({"assigned_to": self.to_person, "department": self.department})
        elif self.movement_type in ("Return", "Disposal"):
            values.update({"assigned_to": "", "department": ""})

        frappe.db.set_value("IT Asset Record", self.asset, values)
