# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from eventsconnect.eventsconnect.utils import get_course_progress


class EventsConnectCourseProgress(Document):
	def after_delete(self):
		progress = get_course_progress(self.course, self.member)
		membership = frappe.db.get_value(
			"Events Connect Enrollment",
			{
				"member": self.member,
				"course": self.course,
			},
			"name",
		)
		frappe.db.set_value("Events Connect Enrollment", membership, "progress", progress)
