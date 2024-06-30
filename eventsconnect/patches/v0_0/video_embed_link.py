import frappe


def execute():
	courses = frappe.get_all(
		"EventsConnect Course", {"video_link": ["is", "set"]}, ["name", "video_link"]
	)
	for course in courses:
		if course.video_link:
			link = course.video_link.split("/")[-1]
			frappe.db.set_value("EventsConnect Course", course.name, "video_link", link)
