# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class EventsConnectMentorRequest(Document):
	def on_update(self):
		if self.has_value_changed("status"):

			if self.status == "Approved":
				self.create_event_mentor_mapping()

			if self.status != "Pending":
				self.send_status_change_email()

	def create_event_mentor_mapping(self):
		mapping = frappe.get_doc(
			{
				"doctype": "EventsConnect Event Mentor Mapping",
				"mentor": self.member,
				"event": self.event,
			}
		)
		mapping.save()

	def send_creation_email(self):
		email_template = self.get_email_template("mentor_request_creation")
		if not email_template:
			return

		event_details = frappe.db.get_value(
			"EventsConnect Event", self.event, ["owner", "slug", "title"], as_dict=True
		)
		message = frappe.render_template(
			email_template.response,
			{
				"member_name": frappe.db.get_value("User", frappe.session.user, "full_name"),
				"event_url": "/eventsconnect/events/" + event_details.slug,
				"event": event_details.title,
			},
		)

		email_args = {
			"recipients": [frappe.session.user, event_details.owner],
			"subject": email_template.subject,
			"header": email_template.subject,
			"message": message,
		}
		frappe.enqueue(
			method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args
		)

	def send_status_change_email(self):
		email_template = self.get_email_template("mentor_request_status_update")
		if not email_template:
			return

		event_details = frappe.db.get_value(
			"EventsConnect Event", self.event, ["owner", "title"], as_dict=True
		)
		message = frappe.render_template(
			email_template.response,
			{
				"member_name": self.member_name,
				"status": self.status,
				"event": event_details.title,
			},
		)

		if self.status == "Approved" or self.status == "Rejected":
			email_args = {
				"recipients": self.member,
				"cc": [event_details.owner, self.reviewed_by],
				"subject": email_template.subject,
				"header": email_template.subject,
				"message": message,
			}
			frappe.enqueue(
				method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args
			)

		elif self.status == "Withdrawn":
			email_args = {
				"recipients": [self.member, event_details.owner],
				"subject": email_template.subject,
				"header": email_template.subject,
				"message": message,
			}
			frappe.enqueue(
				method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args
			)

	def get_email_template(self, template_name):
		template = frappe.db.get_single_value("EventsConnect Settings", template_name)
		if template:
			return frappe.get_doc("Email Template", template)


@frappe.whitelist()
def has_requested(event):
	return frappe.db.count(
		"EventsConnect Mentor Request",
		filters={
			"member": frappe.session.user,
			"event": event,
			"status": ["in", ("Pending", "Approved")],
		},
	)


@frappe.whitelist()
def create_request(event):
	if not has_requested(event):
		request = frappe.get_doc(
			{
				"doctype": "EventsConnect Mentor Request",
				"member": frappe.session.user,
				"event": event,
				"status": "Pending",
			}
		)
		request.save(ignore_permissions=True)
		request.send_creation_email()
		return "OK"

	else:
		return "Already Applied"


@frappe.whitelist()
def cancel_request(event):
	request = frappe.get_doc(
		"EventsConnect Mentor Request",
		{
			"member": frappe.session.user,
			"event": event,
			"status": ["in", ("Pending", "Approved")],
		},
	)
	request.status = "Withdrawn"
	request.save(ignore_permissions=True)
	return "OK"
