// Copyright (c) 2023, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Events Connect Timetable Template", {
	refresh(frm) {
		frm.set_query("reference_doctype", "timetable", function () {
			let doctypes = ["Course Lesson", "Events Connect Quiz", "Events Connect Assignment"];
			return {
				filters: {
					name: ["in", doctypes],
				},
			};
		});

		frm.set_query("reference_doctype", "timetable_legends", function () {
			let doctypes = [
				"Course Lesson",
				"Events Connect Quiz",
				"Events Connect Assignment",
				"Events Connect Live Class",
			];
			return {
				filters: {
					name: ["in", doctypes],
				},
			};
		});
	},
});
