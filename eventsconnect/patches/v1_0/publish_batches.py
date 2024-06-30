import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_batch")
	batches = frappe.get_all("Events Connect Batch", pluck="name")

	for batch in batches:
		frappe.db.set_value("Events Connect Batch", batch, "Published", 1)
