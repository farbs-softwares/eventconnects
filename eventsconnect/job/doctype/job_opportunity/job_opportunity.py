# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form, add_months, getdate
from frappe.utils.user import get_system_managers

from eventsconnect.eventsconnect.utils import validate_image


class EventJobOpportunity(Document):
	def validate(self):
		self.validate_urls()
		self.company_logo = validate_image(self.company_logo)

	def validate_urls(self):
		frappe.utils.validate_url(self.company_website, True)


def update_eventjob_openings():
	old_eventjobs = frappe.get_all(
		"EventJob Opportunity",
		filters={"status": "Open", "creation": ["<=", add_months(getdate(), -3)]},
		pluck="name",
	)

	for eventjob in old_eventjobs:
		frappe.db.set_value("EventJob Opportunity", eventjob, "status", "Closed")


@frappe.whitelist()
def report(eventjob, reason):
	system_managers = get_system_managers(only_name=True)
	user = frappe.db.get_value("User", frappe.session.user, "full_name")
	subject = _("User {0} has reported the eventjob post {1}").format(user, eventjob)
	args = {
		"eventjob": eventjob,
		"eventjob_url": get_link_to_form("EventJob Opportunity", eventjob),
		"user": user,
		"reason": reason,
	}
	frappe.sendmail(
		recipients=system_managers,
		subject=subject,
		header=[subject, "green"],
		template="eventjob_report",
		args=args,
		now=True,
	)
