# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import (
	format_date,
	format_time,
	getdate,
	add_to_date,
	get_datetime,
	nowtime,
	get_time,
)
from eventsconnect.eventsconnect.utils import get_evaluator
import json


class EventsConnectCertificateRequest(Document):
	def validate(self):
		self.set_evaluator()
		self.validate_unavailability()
		self.validate_slot()
		self.validate_if_existing_requests()
		self.validate_evaluation_end_date()

	def set_evaluator(self):
		if not self.evaluator:
			self.evaluator = get_evaluator(self.event, self.batch_name)

	def validate_unavailability(self):
		unavailable = frappe.db.get_value(
			"Event Evaluator", self.evaluator, ["unavailable_from", "unavailable_to"], as_dict=1
		)
		if (
			unavailable.unavailable_from
			and unavailable.unavailable_to
			and getdate(self.date) >= unavailable.unavailable_from
			and getdate(self.date) <= unavailable.unavailable_to
		):
			frappe.throw(
				_(
					"Evaluator is unavailable from {0} to {1}. Please select a date after {1}"
				).format(
					format_date(unavailable.unavailable_from, "medium"),
					format_date(unavailable.unavailable_to, "medium"),
				)
			)

	def validate_slot(self):
		if frappe.db.exists(
			"EventsConnect Certificate Request",
			{
				"evaluator": self.evaluator,
				"date": self.date,
				"start_time": self.start_time,
			},
		):
			frappe.throw(_("The slot is already booked by another participant."))

	def validate_if_existing_requests(self):
		existing_requests = frappe.get_all(
			"EventsConnect Certificate Request",
			{
				"member": self.member,
				"event": self.event,
				"name": ["!=", self.name],
			},
			["date", "start_time", "event"],
		)

		for req in existing_requests:
			if (
				req.date == getdate(self.date)
				or getdate() < getdate(req.date)
				or (
					getdate() == getdate(req.date)
					and getdate(self.start_time) < getdate(req.start_time)
				)
			):
				event_title = frappe.db.get_value("EventsConnect Event", req.event, "title")
				frappe.throw(
					_("You already have an evaluation on {0} at {1} for the event {2}.").format(
						format_date(req.date, "medium"),
						format_time(req.start_time, "short"),
						event_title,
					)
				)
		if getdate() == getdate(self.date) and get_time(self.start_time) < get_time(
			nowtime()
		):
			frappe.throw(_("You cannot schedule evaluations for past slots."))

	def validate_evaluation_end_date(self):
		if self.batch_name:
			evaluation_end_date = frappe.db.get_value(
				"EventsConnect Batch", self.batch_name, "evaluation_end_date"
			)

			if evaluation_end_date:
				if getdate(self.date) > getdate(evaluation_end_date):
					frappe.throw(
						_("You cannot schedule evaluations after {0}.").format(
							format_date(evaluation_end_date, "medium")
						)
					)


def schedule_evals():
	if frappe.db.get_single_value("EventsConnect Settings", "send_calendar_invite_for_evaluations"):
		timelapse = add_to_date(get_datetime(), hours=-5)
		evals = frappe.get_all(
			"EventsConnect Certificate Request",
			{"creation": [">=", timelapse], "google_meet_link": ["is", "not set"]},
			["name", "member", "member_name", "evaluator", "date", "start_time", "end_time"],
		)
		for eval in evals:
			setup_calendar_event(eval)


@frappe.whitelist()
def setup_calendar_event(eval):
	if isinstance(eval, str):
		eval = frappe._dict(json.loads(eval))

	calendar = frappe.db.get_value(
		"Google Calendar", {"user": eval.evaluator, "enable": 1}, "name"
	)

	if calendar:
		event = create_event(eval)
		add_participants(eval, event)
		update_meeting_details(eval, event, calendar)


def create_event(eval):
	event = frappe.get_doc(
		{
			"doctype": "Event",
			"subject": f"Evaluation of {eval.member_name}",
			"starts_on": f"{eval.date} {eval.start_time}",
			"ends_on": f"{eval.date} {eval.end_time}",
		}
	)
	event.save()
	return event


def add_participants(eval, event):
	participants = [eval.member, eval.evaluator]
	for participant in participants:
		contact_name = frappe.db.get_value("Contact", {"email_id": participant}, "name")
		frappe.get_doc(
			{
				"doctype": "Event Participants",
				"reference_doctype": "Contact",
				"reference_docname": contact_name,
				"email": participant,
				"parent": event.name,
				"parenttype": "Event",
				"parentfield": "event_participants",
			}
		).save()


def update_meeting_details(eval, event, calendar):
	event.reload()
	event.update(
		{
			"sync_with_google_calendar": 1,
			"add_video_conferencing": 1,
			"google_calendar": calendar,
		}
	)

	event.save()
	event.reload()
	frappe.db.set_value(
		"EventsConnect Certificate Request", eval.name, "google_meet_link", event.google_meet_link
	)


@frappe.whitelist()
def create_certificate_request(
	event, date, day, start_time, end_time, batch_name=None
):
	is_member = frappe.db.exists(
		{"doctype": "EventsConnect Enrollment", "event": event, "member": frappe.session.user}
	)

	if not is_member:
		return
	eval = frappe.new_doc("EventsConnect Certificate Request")
	eval.update(
		{
			"event": event,
			"evaluator": get_evaluator(event, batch_name),
			"member": frappe.session.user,
			"date": date,
			"day": day,
			"start_time": start_time,
			"end_time": end_time,
			"batch_name": batch_name,
		}
	)
	eval.save(ignore_permissions=True)


@frappe.whitelist()
def create_eventsconnect_certificate_evaluation(source_name, target_doc=None):
	doc = get_mapped_doc(
		"EventsConnect Certificate Request",
		source_name,
		{"EventsConnect Certificate Request": {"doctype": "EventsConnect Certificate Evaluation"}},
		target_doc,
	)
	return doc
