// Copyright (c) 2016, FOSS United and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Event Progress Summary"] = {
	filters: [
		{
			fieldname: "event",
			label: __("Event"),
			fieldtype: "Link",
			options: "EventsConnect Event",
			reqd: 1,
		},
	],
};
