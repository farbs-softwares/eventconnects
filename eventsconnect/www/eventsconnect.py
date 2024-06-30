import frappe
from frappe.utils.telemetry import capture
from frappe import _
from bs4 import BeautifulSoup
import re

no_cache = 1


def get_context():
	app_path = frappe.form_dict.get("app_path")
	context = frappe._dict()
	if app_path:
		context.meta = get_meta(app_path)
	else:
		context.meta = {}
	csrf_token = frappe.sessions.get_csrf_token()
	frappe.db.commit()  # nosemgrep
	context.csrf_token = csrf_token
	if frappe.session.user != "Guest":
		capture("active_site", "eventsconnect")
	return context


def get_meta(app_path):
	if app_path == "events":
		return {
			"title": _("Event List"),
			"image": frappe.db.get_single_value("Website Settings", "banner_image"),
			"description": "This page lists all the events published on our website",
			"keywords": "All Courses, Courses, Learn",
			"link": "/events",
		}

	if re.match(r"^events/.*$", app_path):
		if "new/edit" in app_path:
			return {
				"title": _("New Event"),
				"image": frappe.db.get_single_value("Website Settings", "banner_image"),
				"description": "Create a new event",
				"keywords": "New Event, Create Event",
				"link": "/eventsconnect/events/new/edit",
			}
		event_name = app_path.split("/")[1]
		event = frappe.db.get_value(
			"EventsConnect Event",
			event_name,
			["title", "image", "short_introduction", "tags"],
			as_dict=True,
		)
		return {
			"title": event.title,
			"image": event.image,
			"description": event.short_introduction,
			"keywords": event.tags,
			"link": f"/events/{event_name}",
		}

	if app_path == "batches":
		return {
			"title": _("Batches"),
			"image": frappe.db.get_single_value("Website Settings", "banner_image"),
			"description": "This page lists all the batches published on our website",
			"keywords": "All Batches, Batches, Learn",
			"link": "/batches",
		}
	if re.match(r"^batches/details/.*$", app_path):
		batch_name = app_path.split("/")[2]
		batch = frappe.db.get_value(
			"EventsConnect Batch",
			batch_name,
			["title", "meta_image", "description", "category", "medium"],
			as_dict=True,
		)
		return {
			"title": batch.title,
			"image": batch.meta_image,
			"description": batch.description,
			"keywords": f"{batch.category} {batch.medium}",
			"link": f"/batches/details/{batch_name}",
		}

	if re.match(r"^batches/.*$", app_path):
		batch_name = app_path.split("/")[1]
		if "new/edit" in app_path:
			return {
				"title": _("New Batch"),
				"image": frappe.db.get_single_value("Website Settings", "banner_image"),
				"description": "Create a new batch",
				"keywords": "New Batch, Create Batch",
				"link": "/eventsconnect/batches/new/edit",
			}
		batch = frappe.db.get_value(
			"EventsConnect Batch",
			batch_name,
			["title", "meta_image", "description", "category", "medium"],
			as_dict=True,
		)
		return {
			"title": batch.title,
			"image": batch.meta_image,
			"description": batch.description,
			"keywords": f"{batch.category} {batch.medium}",
			"link": f"/batches/{batch_name}",
		}

	if app_path == "eventjob-openings":
		return {
			"title": _("EventJob Openings"),
			"image": frappe.db.get_single_value("Website Settings", "banner_image"),
			"description": "This page lists all the eventjob openings published on our website",
			"keywords": "EventJob Openings, EventJobs, Vacancies",
			"link": "/eventjob-openings",
		}

	if re.match(r"^eventjob-openings/.*$", app_path):
		eventjob_opening_name = app_path.split("/")[1]
		eventjob_opening = frappe.db.get_value(
			"EventJob Opportunity",
			eventjob_opening_name,
			["eventjob_title", "company_logo", "company_name"],
			as_dict=True,
		)
		return {
			"title": eventjob_opening.eventjob_title,
			"image": eventjob_opening.company_logo,
			"description": eventjob_opening.company_name,
			"keywords": "EventJob Openings, EventJobs, Vacancies",
			"link": f"/eventjob-openings/{eventjob_opening_name}",
		}

	if app_path == "statistics":
		return {
			"title": _("Statistics"),
			"image": frappe.db.get_single_value("Website Settings", "banner_image"),
			"description": "This page lists all the statistics of this platform",
			"keywords": "Enrollment Count, Completion, Signups",
			"link": "/statistics",
		}

	if re.match(r"^user/.*$", app_path):
		username = app_path.split("/")[1]
		user = frappe.db.get_value(
			"User",
			{
				"username": username,
			},
			["full_name", "user_image", "bio"],
			as_dict=True,
		)

		soup = BeautifulSoup(user.bio, "html.parser")
		user.bio = soup.get_text()

		return {
			"title": user.full_name,
			"image": user.user_image,
			"description": user.bio,
			"keywords": f"{user.full_name}, {user.bio}",
			"link": f"/user/{username}",
		}

	if re.match(r"^badges/.*/.*$", app_path):
		badgeName = app_path.split("/")[1]
		email = app_path.split("/")[2]
		badge = frappe.db.get_value(
			"EventsConnect Badge",
			badgeName,
			["title", "image", "description"],
			as_dict=True,
		)
		return {
			"title": badge.title,
			"image": badge.image,
			"description": badge.description,
			"keywords": f"{badge.title}, {badge.description}",
			"link": f"/badges/{badgeName}/{email}",
		}
