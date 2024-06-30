# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import validate_url, validate_email_address
from frappe.email.doctype.email_template.email_template import get_email_template


class EventsConnectAssignmentSubmission(Document):
	def validate(self):
		self.validate_duplicates()
		self.validate_url()

	def after_insert(self):
		if not frappe.flags.in_test:
			outgoing_email_account = frappe.get_cached_value(
				"Email Account", {"default_outgoing": 1, "enable_outgoing": 1}, "name"
			)
			if outgoing_email_account or frappe.conf.get("mail_login"):
				self.send_mail()

	def validate_duplicates(self):
		if frappe.db.exists(
			"EventsConnect Assignment Submission",
			{"assignment": self.assignment, "member": self.member, "name": ["!=", self.name]},
		):
			lesson_title = frappe.db.get_value("Event Lesson", self.lesson, "title")
			frappe.throw(
				_("Assignment for Lesson {0} by {1} already exists.").format(
					lesson_title, self.member_name
				)
			)

	def validate_url(self):
		if self.type == "URL" and not validate_url(self.answer):
			frappe.throw(_("Please enter a valid URL."))

	def send_mail(self):
		subject = _("New Assignment Submission")
		template = "assignment_submission"
		custom_template = frappe.db.get_single_value(
			"EventsConnect Settings", "assignment_submission_template"
		)

		args = {
			"member_name": self.member_name,
			"assignment_name": self.assignment,
			"assignment_title": self.assignment_title,
			"submission_name": self.name,
		}

		moderators = frappe.get_all("Has Role", {"role": "Moderator"}, pluck="parent")
		for moderator in moderators:
			if not validate_email_address(moderator):
				moderators.remove(moderator)

		if custom_template:
			email_template = get_email_template(custom_template, args)
			subject = email_template.get("subject")
			content = email_template.get("message")
		frappe.sendmail(
			recipients=moderators,
			subject=subject,
			template=template if not custom_template else None,
			content=content if custom_template else None,
			args=args,
			header=[subject, "green"],
		)


@frappe.whitelist()
def upload_assignment(
	assignment_attachment=None,
	answer=None,
	assignment=None,
	lesson=None,
	status="Not Graded",
	comments=None,
	submission=None,
):
	if frappe.session.user == "Guest":
		return

	assignment_details = frappe.db.get_value(
		"EventsConnect Assignment", assignment, ["type", "grade_assignment"], as_dict=1
	)
	assignment_type = assignment_details.type

	if assignment_type in ["URL", "Text"] and not answer:
		frappe.throw(_("Please enter the URL for assignment submission."))

	if assignment_type == "File" and not assignment_attachment:
		frappe.throw(_("Please upload the assignment file."))

	if assignment_type == "URL" and not validate_url(answer):
		frappe.throw(_("Please enter a valid URL."))

	if submission:
		doc = frappe.get_doc("EventsConnect Assignment Submission", submission)
	else:
		doc = frappe.get_doc(
			{
				"doctype": "EventsConnect Assignment Submission",
				"assignment": assignment,
				"lesson": lesson,
				"member": frappe.session.user,
				"type": assignment_type,
			}
		)

	doc.update(
		{
			"assignment_attachment": assignment_attachment,
			"status": "Not Applicable"
			if assignment_type == "Text" and not assignment_details.grade_assignment
			else status,
			"comments": comments,
			"answer": answer,
		}
	)
	doc.save(ignore_permissions=True)
	return doc.name


@frappe.whitelist()
def get_assignment(lesson):
	assignment = frappe.db.get_value(
		"EventsConnect Assignment Submission",
		{"lesson": lesson, "member": frappe.session.user},
		["name", "lesson", "member", "assignment_attachment", "comments", "status"],
		as_dict=True,
	)
	assignment.file_name = frappe.db.get_value(
		"File", {"file_url": assignment.assignment_attachment}, "file_name"
	)
	return assignment


@frappe.whitelist()
def grade_assignment(name, result, comments):
	doc = frappe.get_doc("EventsConnect Assignment Submission", name)
	doc.status = result
	doc.comments = comments
	doc.save(ignore_permissions=True)
