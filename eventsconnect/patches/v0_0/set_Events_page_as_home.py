import frappe


def execute():
	frappe.db.set_value("Portal Settings", None, "default_portal_home", "/events")
	frappe.db.set_value("Role", "Event Instructor", "home_page", "")
	frappe.db.set_value("Role", "Event Moderator", "home_page", "")
