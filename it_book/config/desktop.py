from frappe import _


IT_BOOK_ROLES = ["System Manager", "IT Manager", "IT Officer", "IT Auditor"]


def get_data():
    return [
        {
            "module_name": "IT Book",
            "color": "blue",
            "icon": "octicon octicon-device-desktop",
            "type": "module",
            "label": _("IT Book"),
            "roles": IT_BOOK_ROLES,
        }
    ]