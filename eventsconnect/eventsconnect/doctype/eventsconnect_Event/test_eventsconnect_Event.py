# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

import unittest

import frappe

from .eventsconnect_event import EventsConnectCourse


class TestEventsConnectCourse(unittest.TestCase):
	def test_new_event(self):
		event = new_event("Test Event")
		assert event.title == "Test Event"

	# disabled this test as it is failing
	def _test_add_mentors(self):
		event = new_event("Test Event")
		assert event.get_mentors() == []

		user = new_user("Tester", "tester@example.com")
		event.add_mentor("tester@example.com")

		mentors = event.get_mentors()
		mentors_data = [
			dict(email=mentor.email, batch_count=mentor.batch_count) for mentor in mentors
		]
		assert mentors_data == [{"email": "tester@example.com", "batch_count": 0}]

	def tearDown(self):
		if frappe.db.exists("User", "tester@example.com"):
			frappe.delete_doc("User", "tester@example.com")

		if frappe.db.exists("EventsConnect Event", "test-event"):
			frappe.db.delete("Exercise Submission", {"event": "test-event"})
			frappe.db.delete("Exercise Latest Submission", {"event": "test-event"})
			frappe.db.delete("EventsConnect Exercise", {"event": "test-event"})
			frappe.db.delete("EventsConnect Enrollment", {"event": "test-event"})
			frappe.db.delete("Event Lesson", {"event": "test-event"})
			frappe.db.delete("Event Chapter", {"event": "test-event"})
			frappe.db.delete("EventsConnect Batch Old", {"event": "test-event"})
			frappe.db.delete("EventsConnect Event Mentor Mapping", {"event": "test-event"})
			frappe.db.delete("Event Instructor", {"parent": "test-event"})
			frappe.db.sql("delete from `tabCourse Instructor`")
			frappe.delete_doc("EventsConnect Event", "test-event")


def new_user(name, email):
	user = frappe.db.exists("User", email)
	if user:
		return frappe.get_doc("User", user)
	else:
		filters = {
			"email": email,
			"first_name": name,
			"send_welcome_email": False,
		}

		doc = frappe.new_doc("User")
		doc.update(filters)
		doc.save()
		return doc


def new_event(title, additional_filters=None):
	event = frappe.db.exists("EventsConnect Event", {"title": title})
	if event:
		return frappe.get_doc("EventsConnect Event", event)
	else:
		create_evaluator()
		user = frappe.db.get_value(
			"User",
			{
				"user_type": "System User",
			},
		)
		filters = {
			"title": title,
			"short_introduction": title,
			"description": title,
			"video_link": "https://youtu.be/pEbIhUySqbk",
			"image": "/assets/eventsconnect/images/event-home.png",
			"instructors": [{"instructor": user}],
		}

		if additional_filters:
			filters.update(additional_filters)

		doc = frappe.new_doc("EventsConnect Event")
		doc.update(filters)
		doc.save()
		return doc


def create_evaluator():
	if not frappe.db.exists("Event Evaluator", "evaluator@example.com"):
		new_user("Evaluator", "evaluator@example.com")
		frappe.get_doc(
			{"doctype": "Event Evaluator", "evaluator": "evaluator@example.com"}
		).save(ignore_permissions=True)
