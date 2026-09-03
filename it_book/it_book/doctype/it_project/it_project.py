import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate


class ITProject(Document):
    def validate(self):
        self.validate_progress()
        self.set_budget_utilization()
        self.set_alert_status()

    def validate_progress(self):
        if self.progress is not None and flt(self.progress) < 0:
            frappe.throw("Progress cannot be less than 0%.")

    def set_budget_utilization(self):
        planned_budget = flt(self.planned_budget)
        actual_spend = flt(self.actual_spend)
        self.budget_utilization = (actual_spend / planned_budget * 100) if planned_budget else 0

    def set_alert_status(self):
        if flt(self.progress) > 100:
            self.alert_status = "Unrealistic Report"
            return

        if flt(self.budget_utilization) > 100 and self.status not in ("Completed", "Cancelled"):
            self.alert_status = "Budget Risk"
            return

        if self.due_date and getdate(self.due_date) < getdate(nowdate()) and self.status not in ("Completed", "Cancelled"):
            self.alert_status = "Overdue"
            return

        if not self.alert_status or self.alert_status in ("Overdue", "Unrealistic Report", "Budget Risk"):
            self.alert_status = "Healthy"
