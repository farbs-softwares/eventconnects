from . import __version__ as app_version

app_name = "frappe_eventsconnect"
app_title = "Frappe Events Connect"
app_publisher = "Frappe"
app_description = "Frappe Events Connect App"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "school@frappe.io"
app_license = "AGPL"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/eventsconnect/css/eventsconnect.css"
# app_include_js = "/assets/eventsconnect/js/eventsconnect.js"

# include js, css files in header of web template
web_include_css = "eventsconnect.bundle.css"
# web_include_css = "/assets/eventsconnect/css/eventsconnect.css"
web_include_js = ["website.bundle.js"]

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "eventsconnect/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "eventsconnect.install.before_install"
after_install = "eventsconnect.install.after_install"
after_sync = "eventsconnect.install.after_sync"
before_uninstall = "eventsconnect.install.before_uninstall"


setup_wizard_requires = "assets/eventsconnect/js/setup_wizard.js"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "eventsconnect.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"User": "eventsconnect.overrides.user.CustomUser",
	"Web Template": "eventsconnect.overrides.web_template.CustomWebTemplate",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		"on_change": [
			"eventsconnect.eventsconnect.doctype.eventsconnect_badge.eventsconnect_badge.process_badges",
		]
	},
	"Discussion Reply": {"after_insert": "eventsconnect.eventsconnect.utils.handle_notifications"},
	"Notification Log": {"on_change": "eventsconnect.eventsconnect.utils.publish_notifications"},
}

# Scheduled Tasks
# ---------------
scheduler_events = {
	"hourly": [
		"eventsconnect.eventsconnect.doctype.eventsconnect_certificate_request.eventsconnect_certificate_request.schedule_evals"
	],
	"daily": ["eventsconnect.eventjob.doctype.eventjob_opportunity.eventjob_opportunity.update_eventjob_openings"],
}

fixtures = ["Custom Field", "Function", "Industry"]

# Testing
# -------

# before_tests = "eventsconnect.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	# "frappe.desk.search.get_names_for_mentions": "eventsconnect.eventsconnect.utils.get_names_for_mentions",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "eventsconnect.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Add all simple route rules here
website_route_rules = [
	{"from_route": "/eventsconnect/<path:app_path>", "to_route": "eventsconnect"},
	{
		"from_route": "/courses/<course_name>/<certificate_id>",
		"to_route": "certificate",
	},
]

website_redirects = [
	{"source": "/update-profile", "target": "/edit-profile"},
	{"source": "/courses", "target": "/eventsconnect/courses"},
	{
		"source": r"^/courses/.*$",
		"target": "/eventsconnect/courses",
	},
	{"source": "/batches", "target": "/eventsconnect/batches"},
	{
		"source": r"/batches/(.*)",
		"target": "/eventsconnect/batches",
		"match_with_query_string": True,
	},
	{"source": "/eventjob-openings", "target": "/eventsconnect/eventjob-openings"},
	{
		"source": r"/eventjob-openings/(.*)",
		"target": "/eventsconnect/eventjob-openings",
		"match_with_query_string": True,
	},
	{"source": "/statistics", "target": "/eventsconnect/statistics"},
]

update_website_context = [
	"eventsconnect.widgets.update_website_context",
]

jinja = {
	"methods": [
		"eventsconnect.page_renderers.get_profile_url",
		"eventsconnect.overrides.user.get_enrolled_courses",
		"eventsconnect.overrides.user.get_course_membership",
		"eventsconnect.overrides.user.get_authored_courses",
		"eventsconnect.overrides.user.get_palette",
		"eventsconnect.eventsconnect.utils.get_membership",
		"eventsconnect.eventsconnect.utils.get_lessons",
		"eventsconnect.eventsconnect.utils.get_tags",
		"eventsconnect.eventsconnect.utils.get_instructors",
		"eventsconnect.eventsconnect.utils.get_students",
		"eventsconnect.eventsconnect.utils.get_average_rating",
		"eventsconnect.eventsconnect.utils.is_certified",
		"eventsconnect.eventsconnect.utils.get_lesson_index",
		"eventsconnect.eventsconnect.utils.get_lesson_url",
		"eventsconnect.eventsconnect.utils.get_chapters",
		"eventsconnect.eventsconnect.utils.get_slugified_chapter_title",
		"eventsconnect.eventsconnect.utils.get_progress",
		"eventsconnect.eventsconnect.utils.render_html",
		"eventsconnect.eventsconnect.utils.is_mentor",
		"eventsconnect.eventsconnect.utils.is_cohort_staff",
		"eventsconnect.eventsconnect.utils.get_mentors",
		"eventsconnect.eventsconnect.utils.get_reviews",
		"eventsconnect.eventsconnect.utils.is_eligible_to_review",
		"eventsconnect.eventsconnect.utils.get_initial_members",
		"eventsconnect.eventsconnect.utils.get_sorted_reviews",
		"eventsconnect.eventsconnect.utils.is_instructor",
		"eventsconnect.eventsconnect.utils.convert_number_to_character",
		"eventsconnect.eventsconnect.utils.get_signup_optin_checks",
		"eventsconnect.eventsconnect.utils.get_popular_courses",
		"eventsconnect.eventsconnect.utils.format_amount",
		"eventsconnect.eventsconnect.utils.first_lesson_exists",
		"eventsconnect.eventsconnect.utils.get_courses_under_review",
		"eventsconnect.eventsconnect.utils.has_course_instructor_role",
		"eventsconnect.eventsconnect.utils.has_course_moderator_role",
		"eventsconnect.eventsconnect.utils.get_certificates",
		"eventsconnect.eventsconnect.utils.format_number",
		"eventsconnect.eventsconnect.utils.get_lesson_count",
		"eventsconnect.eventsconnect.utils.get_all_memberships",
		"eventsconnect.eventsconnect.utils.get_filtered_membership",
		"eventsconnect.eventsconnect.utils.show_start_learing_cta",
		"eventsconnect.eventsconnect.utils.can_create_courses",
		"eventsconnect.eventsconnect.utils.get_telemetry_boot_info",
		"eventsconnect.eventsconnect.utils.is_onboarding_complete",
		"eventsconnect.www.utils.is_student",
	],
	"filters": [],
}
## Specify the additional tabs to be included in the user profile page.
## Each entry must be a subclass of eventsconnect.eventsconnect.plugins.ProfileTab
# profile_tabs = []

## Specify the extension to be used to control what scripts and stylesheets
## to be included in lesson pages. The specified value must be be a
## subclass of eventsconnect.plugins.PageExtension
# eventsconnect_lesson_page_extension = None

# eventsconnect_lesson_page_extensions = [
# 	"eventsconnect.plugins.LiveCodeExtension"
# ]

has_website_permission = {
	"Events Connect Certificate Evaluation": "eventsconnect.eventsconnect.doctype.eventsconnect_certificate_evaluation.eventsconnect_certificate_evaluation.has_website_permission",
	"Events Connect Certificate": "eventsconnect.eventsconnect.doctype.eventsconnect_certificate.eventsconnect_certificate.has_website_permission",
}

## Markdown Macros for Lessons
eventsconnect_markdown_macro_renderers = {
	"Exercise": "eventsconnect.plugins.exercise_renderer",
	"Quiz": "eventsconnect.plugins.quiz_renderer",
	"YouTubeVideo": "eventsconnect.plugins.youtube_video_renderer",
	"Video": "eventsconnect.plugins.video_renderer",
	"Assignment": "eventsconnect.plugins.assignment_renderer",
	"Embed": "eventsconnect.plugins.embed_renderer",
	"Audio": "eventsconnect.plugins.audio_renderer",
	"PDF": "eventsconnect.plugins.pdf_renderer",
}

# page_renderer to manage profile pages
page_renderer = [
	"eventsconnect.page_renderers.ProfileRedirectPage",
	"eventsconnect.page_renderers.ProfilePage",
	"eventsconnect.page_renderers.CoursePage",
]

# set this to "/" to have profiles on the top-level
profile_url_prefix = "/users/"

signup_form_template = "eventsconnect.plugins.show_custom_signup"

on_session_creation = "eventsconnect.overrides.user.on_session_creation"
