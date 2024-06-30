# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import json
import random
import frappe
from frappe.model.document import Document
from frappe.utils import cint, today
from frappe.utils.telemetry import capture
from eventsconnect.eventsconnect.utils import get_chapters, can_create_events
from ...utils import generate_slug, validate_image
from frappe import _


class EventsConnectCourse(Document):
	def validate(self):
		self.validate_published()
		self.validate_instructors()
		self.validate_video_link()
		self.validate_status()
		self.image = validate_image(self.image)

	def validate_published(self):
		if self.published and not self.published_on:
			self.published_on = today()

	def validate_instructors(self):
		if self.is_new() and not self.instructors:
			frappe.get_doc(
				{
					"doctype": "Event Instructor",
					"instructor": self.owner,
					"parent": self.name,
					"parentfield": "instructors",
					"parenttype": "EventsConnect Event",
				}
			).save(ignore_permissions=True)

	def validate_video_link(self):
		if self.video_link and "/" in self.video_link:
			self.video_link = self.video_link.split("/")[-1]

	def validate_status(self):
		if self.published:
			self.status = "Approved"

	def on_update(self):
		if not self.upcoming and self.has_value_changed("upcoming"):
			self.send_email_to_interested_users()

	def after_insert(self):
		capture("event_created", "eventsconnect")

	def send_email_to_interested_users(self):
		interested_users = frappe.get_all(
			"EventsConnect Event Interest", {"event": self.name}, ["name", "user"]
		)
		subject = self.title + " is available!"
		args = {
			"title": self.title,
			"event_link": f"/eventsconnect/events/{self.name}",
			"app_name": frappe.db.get_single_value("System Settings", "app_name"),
			"site_url": frappe.utils.get_url(),
		}

		for user in interested_users:
			args["first_name"] = frappe.db.get_value("User", user.user, "first_name")
			email_args = frappe._dict(
				recipients=user.user,
				subject=subject,
				header=[subject, "green"],
				template="eventsconnect_event_interest",
				args=args,
				now=True,
			)
			frappe.enqueue(
				method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args
			)
			frappe.db.set_value("EventsConnect Event Interest", user.name, "email_sent", True)

	def autoname(self):
		if not self.name:
			title = self.title
			if self.title == "New Event":
				title = self.title + str(random.randint(0, 99))
			self.name = generate_slug(title, "EventsConnect Event")

	def __repr__(self):
		return f"<Event#{self.name}>"

	def has_mentor(self, email):
		"""Checks if this event has a mentor with given email."""
		if not email or email == "Guest":
			return False

		mapping = frappe.get_all(
			"EventsConnect Event Mentor Mapping", {"event": self.name, "mentor": email}
		)
		return mapping != []

	def add_mentor(self, email):
		"""Adds a new mentor to the event."""
		if not email:
			raise ValueError("Invalid email")
		if email == "Guest":
			raise ValueError("Guest user can not be added as a mentor")

		# given user is already a mentor
		if self.has_mentor(email):
			return

		doc = frappe.get_doc(
			{"doctype": "EventsConnect Event Mentor Mapping", "event": self.name, "mentor": email}
		)
		doc.insert()

	def get_student_batch(self, email):
		"""Returns the batch the given student is part of.

		Returns None if the student is not part of any batch.
		"""
		if not email:
			return

		batch_name = frappe.get_value(
			doctype="EventsConnect Enrollment",
			filters={"event": self.name, "member_type": "Student", "member": email},
			fieldname="batch_old",
		)
		return batch_name and frappe.get_doc("EventsConnect Batch Old", batch_name)

	def get_batches(self, mentor=None):
		batches = frappe.get_all("EventsConnect Batch Old", {"event": self.name})
		if mentor:
			# TODO: optimize this
			memberships = frappe.db.get_all("EventsConnect Enrollment", {"member": mentor}, ["batch_old"])
			batch_names = {m.batch_old for m in memberships}
			return [b for b in batches if b.name in batch_names]

	def get_cohorts(self):
		return frappe.get_all(
			"Cohort",
			{"event": self.name},
			["name", "slug", "title", "begin_date", "end_date"],
			order_by="creation",
		)

	def get_cohort(self, cohort_slug):
		name = frappe.get_value("Cohort", {"event": self.name, "slug": cohort_slug})
		return name and frappe.get_doc("Cohort", name)

	def reindex_exercises(self):
		for i, c in enumerate(get_chapters(self.name), start=1):
			self._reindex_exercises_in_chapter(c, i)

	def _reindex_exercises_in_chapter(self, c, index):
		i = 1
		for lesson in self.get_lessons(c):
			for exercise in lesson.get_exercises():
				exercise.index_ = i
				exercise.index_label = f"{index}.{i}"
				exercise.save()
				i += 1

	def get_all_memberships(self, member):
		all_memberships = frappe.get_all(
			"EventsConnect Enrollment", {"member": member, "event": self.name}, ["batch_old"]
		)
		for membership in all_memberships:
			membership.batch_title = frappe.db.get_value(
				"EventsConnect Batch Old", membership.batch_old, "title"
			)
		return all_memberships


@frappe.whitelist()
def reindex_exercises(doc):
	event_data = json.loads(doc)
	event = frappe.get_doc("EventsConnect Event", event_data["name"])
	event.reindex_exercises()
	frappe.msgprint("All exercises in this event have been re-indexed.")


@frappe.whitelist(allow_guest=True)
def search_event(text):
	events = frappe.get_all(
		"EventsConnect Event",
		filters={"published": True},
		or_filters={
			"title": ["like", f"%{text}%"],
			"tags": ["like", f"%{text}%"],
			"short_introduction": ["like", f"%{text}%"],
			"description": ["like", f"%{text}%"],
		},
		fields=["name", "title"],
	)
	return events


@frappe.whitelist()
def submit_for_review(event):
	chapters = frappe.get_all("Chapter Reference", {"parent": event})
	if not len(chapters):
		return "No Chp"
	frappe.db.set_value("EventsConnect Event", event, "status", "Under Review")
	return "OK"


@frappe.whitelist()
def save_event(
	tags,
	title,
	short_introduction,
	video_link,
	description,
	event,
	published,
	upcoming,
	image=None,
	paid_event=False,
	event_price=None,
	currency=None,
):
	if not can_create_events(event):
		return

	if event:
		doc = frappe.get_doc("EventsConnect Event", event)
	else:
		doc = frappe.get_doc({"doctype": "EventsConnect Event"})

	doc.update(
		{
			"title": title,
			"short_introduction": short_introduction,
			"video_link": video_link,
			"image": image,
			"description": description,
			"tags": tags,
			"published": cint(published),
			"upcoming": cint(upcoming),
			"paid_event": cint(paid_event),
			"event_price": event_price,
			"currency": currency,
		}
	)
	doc.save(ignore_permissions=True)
	return doc.name


@frappe.whitelist()
def save_chapter(event, title, chapter_description, idx, chapter):
	if chapter:
		doc = frappe.get_doc("Event Chapter", chapter)
	else:
		doc = frappe.get_doc({"doctype": "Event Chapter"})

	doc.update({"event": event, "title": title, "description": chapter_description})
	doc.save(ignore_permissions=True)

	if chapter:
		chapter_reference = frappe.get_doc("Chapter Reference", {"chapter": chapter})
	else:
		chapter_reference = frappe.get_doc(
			{
				"doctype": "Chapter Reference",
				"parent": event,
				"parenttype": "EventsConnect Event",
				"parentfield": "chapters",
				"idx": idx,
			}
		)

	chapter_reference.update({"chapter": doc.name})
	chapter_reference.save(ignore_permissions=True)

	return doc.name


@frappe.whitelist()
def save_lesson(
	title,
	body,
	chapter,
	preview,
	idx,
	lesson,
	instructor_notes=None,
	youtube=None,
	quiz_id=None,
	question=None,
	file_type=None,
):
	if lesson:
		doc = frappe.get_doc("Event Lesson", lesson)
	else:
		doc = frappe.get_doc({"doctype": "Event Lesson"})

	doc.update(
		{
			"chapter": chapter,
			"title": title,
			"body": body,
			"instructor_notes": instructor_notes,
			"include_in_preview": preview,
			"youtube": youtube,
			"quiz_id": quiz_id,
			"question": question,
			"file_type": file_type,
		}
	)
	doc.save(ignore_permissions=True)

	if lesson:
		lesson_reference = frappe.get_doc("Lesson Reference", {"lesson": lesson})
	else:
		lesson_reference = frappe.get_doc(
			{
				"doctype": "Lesson Reference",
				"parent": chapter,
				"parenttype": "Event Chapter",
				"parentfield": "lessons",
				"idx": idx,
			}
		)

	lesson_reference.update({"lesson": doc.name})
	lesson_reference.save(ignore_permissions=True)

	return doc.name


@frappe.whitelist()
def reorder_lesson(old_chapter, old_lesson_array, new_chapter, new_lesson_array):
	if old_chapter == new_chapter:
		sort_lessons(new_chapter, new_lesson_array)
	else:
		sort_lessons(old_chapter, old_lesson_array)
		sort_lessons(new_chapter, new_lesson_array)


def sort_lessons(chapter, lesson_array):
	lesson_array = json.loads(lesson_array)
	for les in lesson_array:
		ref = frappe.get_all("Lesson Reference", {"lesson": les}, ["name", "idx"])
		if ref:
			frappe.db.set_value(
				"Lesson Reference",
				ref[0].name,
				{
					"parent": chapter,
					"idx": lesson_array.index(les) + 1,
				},
			)


@frappe.whitelist()
def reorder_chapter(chapter_array):
	chapter_array = json.loads(chapter_array)

	for chap in chapter_array:
		ref = frappe.get_all("Chapter Reference", {"chapter": chap}, ["name", "idx"])
		if ref:
			frappe.db.set_value(
				"Chapter Reference",
				ref[0].name,
				{
					"idx": chapter_array.index(chap) + 1,
				},
			)
