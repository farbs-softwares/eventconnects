import frappe
from eventsconnect.install import create_batch_source


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_source")
	create_batch_source()
