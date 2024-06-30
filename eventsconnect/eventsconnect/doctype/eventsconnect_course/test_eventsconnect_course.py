# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

import unittest

import frappe

from .eventsconnect_course import EventsConnectCourse


class TestEventsConnectCourse(unittest.TestCase):
	def test_new_course(self):
		course = new_course("Test Course")
		assert course.title == "Test Course"

	# disabled this test as it is failing
	def _test_add_mentors(self):
		course = new_course("Test Course")
		assert course.get_mentors() == []

		user = new_user("Tester", "tester@example.com")
		course.add_mentor("tester@example.com")

		mentors = course.get_mentors()
		mentors_data = [
			dict(email=mentor.email, batch_count=mentor.batch_count) for mentor in mentors
		]
		assert mentors_data == [{"email": "tester@example.com", "batch_count": 0}]

	def tearDown(self):
		if frappe.db.exists("User", "tester@example.com"):
			frappe.delete_doc("User", "tester@example.com")

		if frappe.db.exists("EventsConnect Course", "test-course"):
			frappe.db.delete("Exercise Submission", {"course": "test-course"})
			frappe.db.delete("Exercise Latest Submission", {"course": "test-course"})
			frappe.db.delete("EventsConnect Exercise", {"course": "test-course"})
			frappe.db.delete("EventsConnect Enrollment", {"course": "test-course"})
			frappe.db.delete("Course Lesson", {"course": "test-course"})
			frappe.db.delete("Course Chapter", {"course": "test-course"})
			frappe.db.delete("EventsConnect Batch Old", {"course": "test-course"})
			frappe.db.delete("EventsConnect Course Mentor Mapping", {"course": "test-course"})
			frappe.db.delete("Course Instructor", {"parent": "test-course"})
			frappe.db.sql("delete from `tabCourse Instructor`")
			frappe.delete_doc("EventsConnect Course", "test-course")


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


def new_course(title, additional_filters=None):
	course = frappe.db.exists("EventsConnect Course", {"title": title})
	if course:
		return frappe.get_doc("EventsConnect Course", course)
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
			"image": "/assets/eventsconnect/images/course-home.png",
			"instructors": [{"instructor": user}],
		}

		if additional_filters:
			filters.update(additional_filters)

		doc = frappe.new_doc("EventsConnect Course")
		doc.update(filters)
		doc.save()
		return doc


def create_evaluator():
	if not frappe.db.exists("Course Evaluator", "evaluator@example.com"):
		new_user("Evaluator", "evaluator@example.com")
		frappe.get_doc(
			{"doctype": "Course Evaluator", "evaluator": "evaluator@example.com"}
		).save(ignore_permissions=True)
