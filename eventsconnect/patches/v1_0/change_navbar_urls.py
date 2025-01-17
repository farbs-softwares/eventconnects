import frappe


def execute():
	rename_link("/events", "/eventsconnect/events")
	rename_link("/batches", "/eventsconnect/batches")
	rename_link("/statistics", "/eventsconnect/statistics")
	rename_link("/eventjob-openings", "/eventsconnect/eventjob-openings")
	delete_link("/people")


def rename_link(source, target):
	link = frappe.db.exists("Top Bar Item", {"url": source})

	if link:
		frappe.db.set_value("Top Bar Item", link, "url", target)


def delete_link(source):
	link = frappe.db.exists("Top Bar Item", {"url": source})

	if link:
		frappe.delete_doc("Top Bar Item", link)
