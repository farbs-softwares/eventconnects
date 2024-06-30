import frappe


def execute():
	frappe.rename_doc("Role", "Instructor", "Event Creator")
