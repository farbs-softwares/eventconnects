# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from eventsconnect.eventsconnect.doctype.eventsconnect_enrollment.eventsconnect_enrollment import create_membership
from eventsconnect.eventsconnect.utils import is_mentor


class EventsConnectBatchOld(Document):
	def validate(self):
		pass
		# self.validate_if_mentor()

	def validate_if_mentor(self):
		if not is_mentor(self.event, frappe.session.user):
			event_title = frappe.db.get_value("EventsConnect Event", self.event, "title")
			frappe.throw(_("You are not a mentor of the event {0}").format(event_title))

	def after_insert(self):
		create_membership(batch=self.name, event=self.event, member_type="Mentor")

	def is_member(self, email, member_type=None):
		"""Checks if a person is part of a batch.

		If member_type is specified, checks if the person is a Student/Mentor.
		"""

		filters = {"batch_old": self.name, "member": email}
		if member_type:
			filters["member_type"] = member_type
		return frappe.db.exists("EventsConnect Enrollment", filters)

	def get_membership(self, email):
		"""Returns the membership document of given user."""
		name = frappe.get_value(
			doctype="EventsConnect Enrollment",
			filters={"batch_old": self.name, "member": email},
			fieldname="name",
		)
		return frappe.get_doc("EventsConnect Enrollment", name)

	def get_current_lesson(self, user):
		"""Returns the name of the current lesson for the given user."""
		membership = self.get_membership(user)
		return membership and membership.current_lesson


@frappe.whitelist()
def save_message(message, batch):
	doc = frappe.get_doc(
		{
			"doctype": "EventsConnect Message",
			"batch_old": batch,
			"author": frappe.session.user,
			"message": message,
		}
	)
	doc.save(ignore_permissions=True)


def switch_batch(event_name, email, batch_name):
	"""Switches the user from the current batch of the event to a new batch."""
	membership = frappe.get_last_doc(
		"EventsConnect Enrollment", filters={"event": event_name, "member": email}
	)

	batch = frappe.get_doc("EventsConnect Batch Old", batch_name)
	if not batch:
		raise ValueError(f"Invalid Batch: {batch_name}")

	if batch.event != event_name:
		raise ValueError("Can not switch batches across events")

	if batch.is_member(email):
		print(f"{email} is already a member of {batch.title}")
		return

	old_batch = frappe.get_doc("EventsConnect Batch Old", membership.batch_old)

	membership.batch_old = batch_name
	membership.save()

	# update exercise submissions
	filters = {"owner": email, "batch_old": old_batch.name}
	for name in frappe.db.get_all("Exercise Submission", filters=filters, pluck="name"):
		doc = frappe.get_doc("Exercise Submission", name)
		print("updating exercise submission", name)
		doc.batch_old = batch_name
		doc.save()
