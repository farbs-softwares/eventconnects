# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

import unittest

import frappe

from eventsconnect.eventsconnect.doctype.eventsconnect_event.test_eventsconnect_event import new_event


class TestEventsConnectExercise(unittest.TestCase):
	def new_exercise(self):
		event = new_event("Test Event")
		member = frappe.get_doc(
			{
				"doctype": "EventsConnect Enrollment",
				"event": event.name,
				"member": frappe.session.user,
			}
		)
		member.insert()
		e = frappe.get_doc(
			{
				"doctype": "EventsConnect Exercise",
				"name": "test-problem",
				"event": event.name,
				"title": "Test Problem",
				"description": "draw a circle",
				"code": "# draw a single cicle",
				"answer": ("# draw a single circle\n" + "circle(100, 100, 50)"),
			}
		)
		e.insert()
		return e

	def test_exercise(self):
		e = self.new_exercise()
		assert e.get_user_submission() is None

	def test_exercise_submission(self):
		e = self.new_exercise()
		submission = e.submit("circle(100, 100, 50)")
		assert submission is not None
		assert submission.exercise == e.name
		assert submission.event == e.event

		user_submission = e.get_user_submission()
		assert user_submission is not None
		assert user_submission.name == submission.name

	def tearDown(self):
		frappe.db.delete("EventsConnect Enrollment")
		frappe.db.delete("Exercise Submission")
		frappe.db.delete("EventsConnect Exercise")
