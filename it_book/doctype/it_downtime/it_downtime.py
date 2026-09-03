import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_seconds


class ITDowntime(Document):
    def validate(self):
        if self.start_time and self.end_time:
            seconds = time_diff_in_seconds(self.end_time, self.start_time)
            if seconds < 0:
                frappe.throw("End Time cannot be before Start Time.")
            self.duration_minutes = round(seconds / 60, 2)

        if self.status == "Resolved" and not self.end_time:
            frappe.throw("End Time is required before marking downtime as Resolved.")
