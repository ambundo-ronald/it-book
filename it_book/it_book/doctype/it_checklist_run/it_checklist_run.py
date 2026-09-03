from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class ITChecklistRun(Document):
    def validate(self):
        self.set_status_from_items()

    def set_status_from_items(self):
        if self.status == "Cancelled":
            return

        items = list(self.items or [])
        if items and all(item.status in ("Done", "Not Applicable") for item in items):
            self.status = "Completed"
            return

        if self.due_date and getdate(self.due_date) < getdate(nowdate()):
            self.status = "Overdue"
            return

        if any(item.status in ("Done", "Blocked") for item in items):
            self.status = "In Progress"
