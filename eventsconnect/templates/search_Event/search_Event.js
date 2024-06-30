frappe.ready(() => {
	$("#search-event").keyup((e) => {
		search_event(e);
	});

	$("#open-search").click((e) => {
		show_search_bar(e);
	});

	$("#search-modal").on("hidden.bs.modal", () => {
		hide_search_bar();
	});

	$(document).keydown(function (e) {
		if ((e.metaKey || e.ctrlKey) && e.key == "k") {
			show_search_bar(e);
		}
	});
});

const search_event = (e) => {
	let input = $(e.currentTarget).val();
	if (input == window.input) return;
	window.input = input;

	if (input.length < 3 || input.trim() == "") {
		$(".result-row").remove();
		return;
	}

	frappe.call({
		method: "eventsconnect.eventsconnect.doctype.eventsconnect_event.eventsconnect_event.search_event",
		args: {
			text: input,
		},
		callback: (data) => {
			render_event_list(data);
		},
	});
};

const render_event_list = (data) => {
	let events = data.message;
	$(".result-row").remove();

	if (!events.length) {
		let element = `<a class="result-row">
			${__("No result found")}
		</a>`;
		$(element).insertAfter("#search-event");
		return;
	}

	for (let i in events) {
		let element = `<a class="result-row" href="/events/${events[i].name}">
			${events[i].title}
		</a>`;
		$(element).insertAfter("#search-event");
	}
};

const show_search_bar = (e) => {
	$("#search-modal").modal("show");
	setTimeout(() => {
		$("#search-event").focus();
	}, 1000);
};

const hide_search_bar = (e) => {
	$("#search-event").val("");
	$(".result-row").remove();
};
