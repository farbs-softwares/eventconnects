# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from eventsconnect.eventsconnect.utils import has_event_moderator_role


class EventsConnectCertificateEvaluation(Document):
	def validate(self):
		self.validate_rating()

	def validate_rating(self):
		if self.status not in ["Pending", "In Progress"] and self.rating == 0:
			frappe.throw(_("Rating cannot be 0"))


def has_website_permission(doc, ptype, user, verbose=False):
	if has_event_moderator_role() or doc.member == frappe.session.user:
		return True
	return False


@frappe.whitelist()
def create_eventsconnect_certificate(source_name, target_doc=None):
	doc = get_mapped_doc(
		"EventsConnect Certificate Evaluation",
		source_name,
		{"EventsConnect Certificate Evaluation": {"doctype": "EventsConnect Certificate"}},
		target_doc,
	)
	return doc
