import frappe
from frappe.model.document import Document


class ITChangeRegister(Document):
    def validate(self):
        if self.status in ("Approved", "In Progress", "Released") and self.risk_level in ("High", "Critical"):
            if not self.rollback_plan:
                frappe.throw("A rollback plan is required for high or critical risk changes.")

        if self.status == "Released" and not self.release_notes:
            frappe.throw("Release notes are required before marking a change as Released.")
