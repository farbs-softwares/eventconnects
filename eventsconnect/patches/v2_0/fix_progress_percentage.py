import frappe
from eventsconnect.eventsconnect.utils import get_course_progress


def execute():
	enrollments = frappe.get_all("EventsConnect Enrollment", fields=["name", "course", "member"])

	for enrollment in enrollments:
		progress = get_course_progress(enrollment.course, enrollment.member)
		frappe.db.set_value("EventsConnect Enrollment", enrollment.name, "progress", progress)
