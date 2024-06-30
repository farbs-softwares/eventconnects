import frappe
from eventsconnect.eventsconnect.utils import get_event_progress


def execute():
	enrollments = frappe.get_all("EventsConnect Enrollment", fields=["name", "event", "member"])

	for enrollment in enrollments:
		progress = get_event_progress(enrollment.event, enrollment.member)
		frappe.db.set_value("EventsConnect Enrollment", enrollment.name, "progress", progress)
