import frappe
from frappe.utils import rounded

from eventsconnect.eventsconnect.utils import get_event_progress


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_batch_membership")
	memberships = frappe.get_all(
		"EventsConnect Enrollment", ["name", "event", "member"], order_by="event"
	)

	if len(memberships):
		current_event = memberships[0].event
		for membership in memberships:
			if current_event != membership.event:
				current_event = membership.event

			progress = rounded(get_event_progress(current_event, membership.member))
			frappe.db.set_value("EventsConnect Enrollment", membership.name, "progress", progress)

	frappe.db.delete("Prepared Report", {"ref_report_doctype": "Event Progress Summary"})
	frappe.db.set_value("Report", "Event Progress Summary", "prepared_report", 0)
