// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Events Connect Certificate Request", {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(
				__("Create Events Connect Certificate Evaluation"),
				() => {
					frappe.model.open_mapped_doc({
						method: "eventsconnect.eventsconnect.doctype.eventsconnect_certificate_request.eventsconnect_certificate_request.create_eventsconnect_certificate_evaluation",
						frm: frm,
					});
				}
			);
		}
		if (!frm.doc.google_meet_link) {
			frm.add_custom_button(__("Generate Google Meet Link"), () => {
				frappe.call({
					method: "eventsconnect.eventsconnect.doctype.eventsconnect_certificate_request.eventsconnect_certificate_request.setup_calendar_event",
					args: {
						eval: frm.doc,
					},
				});
			});
		}
	},

	onload: function (frm) {
		frm.set_query("member", function (doc) {
			return {
				filters: {
					ignore_user_type: 1,
				},
			};
		});
	},
});
