import frappe


def execute():
	eventjobs_link = frappe.db.exists(
		"Top Bar Item",
		{
			"label": "EventJobs",
			"url": "/eventjobs",
			"parent_label": "Explore",
		},
	)

	if eventjobs_link:
		frappe.db.set_value("Top Bar Item", eventjobs_link, "url", "/eventjob-openings")
