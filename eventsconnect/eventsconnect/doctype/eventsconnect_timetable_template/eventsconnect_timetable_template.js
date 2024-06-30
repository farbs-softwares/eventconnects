// Copyright (c) 2023, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("EventsConnect Timetable Template", {
	refresh(frm) {
		frm.set_query("reference_doctype", "timetable", function () {
			let doctypes = ["Event Lesson", "EventsConnect Quiz", "EventsConnect Assignment"];
			return {
				filters: {
					name: ["in", doctypes],
				},
			};
		});

		frm.set_query("reference_doctype", "timetable_legends", function () {
			let doctypes = [
				"Event Lesson",
				"EventsConnect Quiz",
				"EventsConnect Assignment",
				"EventsConnect Live Class",
			];
			return {
				filters: {
					name: ["in", doctypes],
				},
			};
		});
	},
});