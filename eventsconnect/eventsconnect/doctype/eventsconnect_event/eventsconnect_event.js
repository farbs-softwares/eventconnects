// Copyright (c) 2021, FOSS United and contributors
// For license information, please see license.txt

frappe.ui.form.on("EventsConnect Event", {
	onload: function (frm) {
		frm.set_query("chapter", "chapters", function () {
			return {
				filters: {
					event: frm.doc.name,
				},
			};
		});

		frm.set_query("event", "related_events", function () {
			return {
				filters: {
					published: true,
				},
			};
		});
	},
	refresh: (frm) => {
		frm.add_web_link(`/eventsconnect/events/${frm.doc.name}`, "See on Website");

		if (!frm.doc.currency)
			frappe.db
				.get_single_value("EventsConnect Settings", "default_currency")
				.then((value) => {
					frm.set_value("currency", value);
				});
	},
});
