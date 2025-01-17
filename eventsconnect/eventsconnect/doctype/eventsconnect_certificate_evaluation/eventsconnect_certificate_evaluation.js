// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("EventsConnect Certificate Evaluation", {
	refresh: function (frm) {
		if (!frm.is_new() && frm.doc.status == "Pass") {
			frm.add_custom_button(__("Create EventsConnect Certificate"), () => {
				frappe.model.open_mapped_doc({
					method: "eventsconnect.eventsconnect.doctype.eventsconnect_certificate_evaluation.eventsconnect_certificate_evaluation.create_eventsconnect_certificate",
					frm: frm,
				});
			});
		}
	},

	onload: function (frm) {
		frm.set_query("event", function (doc) {
			return {
				filters: {
					enable_certification: true,
					grant_certificate_after: "Evaluation",
				},
			};
		});

		frm.set_query("member", function (doc) {
			return {
				filters: {
					ignore_user_type: 1,
				},
			};
		});
	},
});
