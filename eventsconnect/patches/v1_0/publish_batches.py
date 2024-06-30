import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_batch")
	batches = frappe.get_all("EventsConnect Batch", pluck="name")

	for batch in batches:
		frappe.db.set_value("EventsConnect Batch", batch, "Published", 1)
