import frappe


def execute():
	frappe.db.create_sequence("Batch Event", check_not_exists=True)
	frappe.db.set_next_sequence_val("Batch Event", 500, is_val_used=False)
