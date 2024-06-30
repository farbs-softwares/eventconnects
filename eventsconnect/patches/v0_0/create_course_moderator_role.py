from venv import create

import frappe

from eventsconnect.install import create_moderator_role


def execute():
	create_moderator_role()
