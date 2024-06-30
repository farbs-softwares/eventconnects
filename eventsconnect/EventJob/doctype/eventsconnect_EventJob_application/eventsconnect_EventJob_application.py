# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class EventsConnectEventJobApplication(Document):
	def validate(self):
		self.validate_duplicate()

	def after_insert(self):
		outgoing_email_account = frappe.get_cached_value(
			"Email Account", {"default_outgoing": 1, "enable_outgoing": 1}, "name"
		)
		if outgoing_email_account or frappe.conf.get("mail_login"):
			self.send_email_to_employer()

	def validate_duplicate(self):
		if frappe.db.exists("EventsConnect EventJob Application", {"eventjob": self.eventjob, "user": self.user}):
			frappe.throw(_("You have already applied for this eventjob."))

	def send_email_to_employer(self):
		company_email = frappe.get_value("EventJob Opportunity", self.eventjob, "company_email_address")
		if company_email:
			subject = _("New EventJob Applicant")

			args = {
				"full_name": frappe.db.get_value("User", self.user, "full_name"),
				"eventjob_title": self.eventjob_title,
			}
			resume = frappe.get_doc(
				"File",
				{
					"file_name": self.resume,
				},
			)
			frappe.sendmail(
				recipients=company_email,
				subject=subject,
				template="eventjob_application",
				args=args,
				attachments=[
					{
						"fname": resume.file_name,
						"fcontent": resume.get_content(),
					}
				],
				header=[subject, "green"],
				retry=3,
			)