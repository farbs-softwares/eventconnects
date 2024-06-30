# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

import unittest

import frappe

from eventsconnect.eventsconnect.doctype.eventsconnect_event.test_eventsconnect_event import new_event, new_user


class TestEventsConnectEnrollment(unittest.TestCase):
	def setUp(self):
		frappe.db.delete("EventsConnect Enrollment")
		frappe.db.delete("EventsConnect Batch Old")
		frappe.db.delete("EventsConnect Event Mentor Mapping")
		frappe.db.delete("User", {"email": ("like", "%@test.com")})

	def new_event_batch(self):
		event = new_event("Test Event")

		new_user("Test Mentor", "mentor@test.com")
		# without this, the creating batch will fail
		event.add_mentor("mentor@test.com")

		frappe.session.user = "mentor@test.com"

		batch = frappe.get_doc(
			{
				"doctype": "EventsConnect Batch Old",
				"name": "test-batch",
				"title": "Test Batch",
				"event": event.name,
			}
		)
		batch.insert(ignore_permissions=True)

		frappe.session.user = "Administrator"
		return event, batch

	def add_membership(self, batch_name, member_name, event, member_type="Student"):
		doc = frappe.get_doc(
			{
				"doctype": "EventsConnect Enrollment",
				"batch_old": batch_name,
				"member": member_name,
				"member_type": member_type,
				"event": event,
			}
		)
		doc.insert()
		return doc

	def test_membership(self):
		event, batch = self.new_event_batch()
		member = new_user("Test", "test01@test.com")
		membership = self.add_membership(batch.name, member.name, event.name)

		assert membership.event == event.name
		assert membership.member_name == member.full_name

	def test_membership_change_role(self):
		event, batch = self.new_event_batch()
		member = new_user("Test", "test01@test.com")
		membership = self.add_membership(batch.name, member.name, event.name)

		# it should be possible to change role
		membership.role = "Admin"
		membership.save()
