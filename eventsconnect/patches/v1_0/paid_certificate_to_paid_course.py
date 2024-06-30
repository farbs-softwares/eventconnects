import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course")
	courses = frappe.get_all(
		"EventsConnect Course",
		{"paid_certificate": ["is", "set"]},
		["name", "price_certificate", "currency"],
	)

	for course in courses:
		frappe.db.set_value(
			"EventsConnect Course",
			course.name,
			{
				"paid_course": 1,
				"course_price": course.price_certificate,
				"currency": course.currency,
			},
		)
