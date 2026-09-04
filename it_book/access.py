from __future__ import annotations

import frappe


IT_BOOK_ACCESS_ROLES = {"System Manager", "IT Manager", "IT Officer", "IT Auditor"}


def has_it_book_access(user: str | None = None) -> bool:
    user = user or frappe.session.user
    if user == "Administrator":
        return True
    return bool(IT_BOOK_ACCESS_ROLES.intersection(set(frappe.get_roles(user))))


def require_it_book_access():
    if not has_it_book_access():
        frappe.throw("You are not permitted to access IT Book.", frappe.PermissionError)