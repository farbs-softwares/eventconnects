import frappe


def execute():
	events = frappe.get_all(
		"EventsConnect Event", {"video_link": ["is", "set"]}, ["name", "video_link"]
	)
	for event in events:
		if event.video_link:
			link = event.video_link.split("/")[-1]
			frappe.db.set_value("EventsConnect Event", event.name, "video_link", link)
