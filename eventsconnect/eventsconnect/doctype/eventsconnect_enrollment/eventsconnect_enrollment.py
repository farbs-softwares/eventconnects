# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class EventsConnectEnrollment(Document):
	def validate(self):
		self.validate_membership_in_same_batch()
		self.validate_membership_in_different_batch_same_event()

	def validate_membership_in_same_batch(self):
		filters = {"member": self.member, "event": self.event, "name": ["!=", self.name]}
		if self.batch_old:
			filters["batch_old"] = self.batch_old
		previous_membership = frappe.db.get_value(
			"EventsConnect Enrollment", filters, fieldname=["member_type", "member"], as_dict=1
		)

		if previous_membership:
			member_name = frappe.db.get_value("User", self.member, "full_name")
			event_title = frappe.db.get_value("EventsConnect Event", self.event, "title")
			frappe.throw(
				_("{0} is already a {1} of the event {2}").format(
					member_name, previous_membership.member_type, event_title
				)
			)

	def validate_membership_in_different_batch_same_event(self):
		"""Ensures that a studnet is only part of one batch."""
		# nothing to worry if the member is not a student
		if self.member_type != "Student":
			return

		event = frappe.db.get_value("EventsConnect Batch Old", self.batch_old, "event")
		memberships = frappe.get_all(
			"EventsConnect Enrollment",
			filters={
				"member": self.member,
				"name": ["!=", self.name],
				"member_type": "Student",
				"event": self.event,
			},
			fields=["batch_old", "member_type", "name"],
		)

		if memberships:
			membership = memberships[0]
			member_name = frappe.db.get_value("User", self.member, "full_name")
			frappe.throw(
				_("{0} is already a Student of {1} event through {2} batch").format(
					member_name, event, membership.batch_old
				)
			)


@frappe.whitelist()
def create_membership(
	event, batch=None, member=None, member_type="Student", role="Member"
):
	frappe.get_doc(
		{
			"doctype": "EventsConnect Enrollment",
			"batch_old": batch,
			"event": event,
			"role": role,
			"member_type": member_type,
			"member": member or frappe.session.user,
		}
	).save(ignore_permissions=True)
	return "OK"


@frappe.whitelist()
def update_current_membership(batch, event, member):
	all_memberships = frappe.get_all(
		"EventsConnect Enrollment", {"member": member, "event": event}
	)
	for membership in all_memberships:
		frappe.db.set_value("EventsConnect Enrollment", membership.name, "is_current", 0)

	current_membership = frappe.get_all(
		"EventsConnect Enrollment", {"batch_old": batch, "member": member}
	)
	if len(current_membership):
		frappe.db.set_value("EventsConnect Enrollment", current_membership[0].name, "is_current", 1)
