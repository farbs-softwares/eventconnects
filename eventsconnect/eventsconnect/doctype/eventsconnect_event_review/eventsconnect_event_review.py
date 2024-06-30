# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint


class EventsConnectCourseReview(Document):
	def validate(self):
		self.validate_if_already_reviewed()

	def validate_if_already_reviewed(self):
		if frappe.db.exists(
			"EventsConnect Event Review", {"event": self.event, "owner": self.owner}
		):
			frappe.throw(frappe._("You have already reviewed this event"))


@frappe.whitelist()
def submit_review(rating, review, event):
	out_of_ratings = frappe.db.get_all(
		"DocField", {"parent": "EventsConnect Event Review", "fieldtype": "Rating"}, ["options"]
	)
	out_of_ratings = (len(out_of_ratings) and out_of_ratings[0].options) or 5
	rating = cint(rating) / out_of_ratings
	frappe.get_doc(
		{"doctype": "EventsConnect Event Review", "rating": rating, "review": review, "event": event}
	).save(ignore_permissions=True)
	return "OK"
