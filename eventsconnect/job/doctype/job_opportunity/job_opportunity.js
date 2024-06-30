// Copyright (c) 2021, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("EventJob Opportunity", {
	refresh: (frm) => {
		if (frm.doc.name)
			frm.add_web_link(`/eventjob-openings/${frm.doc.name}`, "See on Website");
	},
});
