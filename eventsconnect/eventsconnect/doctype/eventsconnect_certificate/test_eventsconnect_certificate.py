# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

import unittest

import frappe
from frappe.utils import add_years, cint, nowdate

from eventsconnect.eventsconnect.doctype.eventsconnect_certificate.eventsconnect_certificate import create_certificate
from eventsconnect.eventsconnect.doctype.eventsconnect_course.test_eventsconnect_course import new_course


class TestEventsConnectCertificate(unittest.TestCase):
	def test_certificate_creation(self):
		course = new_course(
			"Test Certificate",
			{
				"enable_certification": 1,
				"expiry": 2,
			},
		)
		certificate = create_certificate(course.name)

		self.assertEqual(certificate.member, "Administrator")
		self.assertEqual(certificate.course, course.name)
		self.assertEqual(certificate.issue_date, nowdate())
		self.assertEqual(certificate.expiry_date, add_years(nowdate(), cint(course.expiry)))

		frappe.db.delete("EventsConnect Certificate", certificate.name)
		frappe.db.delete("EventsConnect Course", course.name)
