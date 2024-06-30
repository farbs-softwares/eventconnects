import frappe


def execute():
	if frappe.db.exists("Role", "Event Instructor"):
		frappe.rename_doc("Role", "Event Instructor", "Instructor")

	if frappe.db.exists("Role", "Event Moderator"):
		frappe.rename_doc("Role", "Event Moderator", "Moderator")
