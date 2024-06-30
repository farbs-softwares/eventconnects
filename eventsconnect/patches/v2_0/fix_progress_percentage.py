import frappe
from eventsconnect.eventsconnect.utils import get_course_progress


def execute():
	enrollments = frappe.get_all("Events Connect Enrollment", fields=["name", "course", "member"])

	for enrollment in enrollments:
		progress = get_course_progress(enrollment.course, enrollment.member)
		frappe.db.set_value("Events Connect Enrollment", enrollment.name, "progress", progress)
