import unittest

import frappe
from frappe.utils import getdate

from eventsconnect.eventsconnect.doctype.eventsconnect_event.test_eventsconnect_event import new_event, new_user

from .utils import get_evaluation_details, slugify


class TestUtils(unittest.TestCase):
	def test_simple(self):
		self.assertEqual(slugify("hello-world"), "hello-world")
		self.assertEqual(slugify("Hello World"), "hello-world")
		self.assertEqual(slugify("Hello, World!"), "hello-world")

	def test_duplicates(self):
		self.assertEqual(slugify("Hello World", ["hello-world"]), "hello-world-2")

		self.assertEqual(
			slugify("Hello World", ["hello-world", "hello-world-2"]), "hello-world-3"
		)

	def test_evaluation_details(self):
		user = new_user("Eval", "eval@test.com")

		event = new_event(
			"Test Evaluation Details",
			{
				"enable_certification": 1,
				"grant_certificate_after": "Evaluation",
				"evaluator": "evaluator@example.com",
				"max_attempts": 3,
				"duration": 2,
				"instructors": [{"instructor": user.name}],
			},
		)

		# Two evaluations failed within max attempts. Check eligibility for a third evaluation
		create_evaluation(user.name, event.name, getdate("21-03-2022"), 0.4, "Fail")
		create_evaluation(user.name, event.name, getdate("12-04-2022"), 0.4, "Fail")
		details = get_evaluation_details(event.name, user.name)
		self.assertTrue(details.eligible)

		# Three evaluations failed within max attempts. Check eligibility for a forth evaluation
		create_evaluation(user.name, event.name, getdate("21-03-2022"), 0.4, "Fail")
		create_evaluation(user.name, event.name, getdate("12-04-2022"), 0.4, "Fail")
		create_evaluation(user.name, event.name, getdate("16-04-2022"), 0.4, "Fail")
		details = get_evaluation_details(event.name, user.name)
		self.assertFalse(details.eligible)

		# Three evaluations failed within max attempts. Check eligibility for a forth evaluation. Different Dates
		create_evaluation(user.name, event.name, getdate("01-03-2022"), 0.4, "Fail")
		create_evaluation(user.name, event.name, getdate("12-04-2022"), 0.4, "Fail")
		create_evaluation(user.name, event.name, getdate("16-04-2022"), 0.4, "Fail")
		details = get_evaluation_details(event.name, user.name)
		self.assertFalse(details.eligible)

		frappe.db.delete("EventsConnect Certificate Evaluation", {"event": event.name})
		frappe.db.delete("EventsConnect Event", event.name)
		frappe.db.delete("User", user.name)


def create_evaluation(user, event, date, rating, status):
	evaluation = frappe.get_doc(
		{
			"doctype": "EventsConnect Certificate Evaluation",
			"member": user,
			"event": event,
			"date": date,
			"start_time": "12:00:00",
			"end_time": "13:00:00",
			"rating": rating,
			"status": status,
		}
	)
	evaluation.save()
