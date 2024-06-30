# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from eventsconnect.eventsconnect.utils import get_event_progress


class EventsConnectCourseProgress(Document):
	def after_delete(self):
		progress = get_event_progress(self.event, self.member)
		membership = frappe.db.get_value(
			"EventsConnect Enrollment",
			{
				"member": self.member,
				"event": self.event,
			},
			"name",
		)
		frappe.db.set_value("EventsConnect Enrollment", membership, "progress", progress)
