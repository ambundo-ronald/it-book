from frappe.model.document import Document


class ITBackupLog(Document):
    def validate(self):
        self.requires_attention = 1 if self.status in ("Failed", "Warning") else 0
