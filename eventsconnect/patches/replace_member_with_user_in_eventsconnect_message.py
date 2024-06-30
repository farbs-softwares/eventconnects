import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_message")
	messages = frappe.get_all("EventsConnect Message", ["author", "name"])
	for message in messages:
		user = frappe.db.get_value(
			"Community Member", message.author, ["email", "full_name"], as_dict=True
		)
		frappe.db.set_value("EventsConnect Message", message.name, "author", user.email)
		frappe.db.set_value("EventsConnect Message", message.name, "author_name", user.full_name)
