import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
	events = frappe.get_all(
		"EventsConnect Event",
		{"paid_certificate": ["is", "set"]},
		["name", "price_certificate", "currency"],
	)

	for event in events:
		frappe.db.set_value(
			"EventsConnect Event",
			event.name,
			{
				"paid_event": 1,
				"event_price": event.price_certificate,
				"currency": event.currency,
			},
		)
