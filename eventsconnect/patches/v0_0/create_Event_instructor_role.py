import frappe
from eventsconnect.install import create_event_creator_role


def execute():
	create_event_creator_role()
