import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
	frappe.reload_doc("eventsconnect", "doctype", "event_instructor")
	events = frappe.get_all("EventsConnect Event", fields=["name", "instructor"])
	for event in events:
		doc = frappe.get_doc(
			{
				"doctype": "Event Instructor",
				"parent": event.name,
				"parentfield": "instructors",
				"parenttype": "EventsConnect Event",
				"instructor": event.instructor,
			}
		)
		doc.save()
