"""Handy module to make access to all doctypes from a single place.
"""
from .doctype.eventsconnect_enrollment.eventsconnect_enrollment import (
	EventsConnectBatchMembership as Membership,
)
from .doctype.eventsconnect_event.eventsconnect_event import EventsConnectCourse as Event
