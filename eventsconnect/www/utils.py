import frappe

from eventsconnect.eventsconnect.utils import get_lesson_url, get_lessons, get_membership
from frappe.utils import cstr
from eventsconnect.eventsconnect.utils import redirect_to_events_list


def get_common_context(context):
	context.no_cache = 1

	try:
		batch_name = frappe.form_dict["batch"]
	except KeyError:
		batch_name = None

	event = frappe.db.get_value(
		"EventsConnect Event",
		frappe.form_dict["event"],
		["name", "title", "video_link", "enable_certification", "status"],
		as_dict=True,
	)
	if not event:
		redirect_to_events_list()

	context.event = event
	context.lessons = get_lessons(event.name)
	membership = get_membership(event.name, frappe.session.user, batch_name)
	context.membership = membership
	context.progress = frappe.utils.cint(membership.progress) if membership else 0
	context.batch_old = (
		membership.batch_old if membership and membership.batch_old else None
	)
	context.event.query_parameter = (
		"?batch=" + membership.batch_old if membership and membership.batch_old else ""
	)
	context.livecode_url = get_livecode_url()


def get_livecode_url():
	return frappe.db.get_single_value("EventsConnect Settings", "livecode_url")


def redirect_to_lesson(event, index_="1.1"):
	frappe.local.flags.redirect_location = (
		get_lesson_url(event.name, index_) + event.query_parameter
	)
	raise frappe.Redirect


def get_current_lesson_details(lesson_number, context, is_edit=False):
	details_list = list(filter(lambda x: cstr(x.number) == lesson_number, context.lessons))

	if not len(details_list):
		if is_edit:
			return None
		else:
			redirect_to_lesson(context.event)

	lesson_info = details_list[0]
	lesson_info.body = lesson_info.body.replace('"', "'")
	return lesson_info


def is_student(batch, member=None):
	if not member:
		member = frappe.session.user

	return frappe.db.exists(
		"Batch Student",
		{
			"student": member,
			"parent": batch,
		},
	)
