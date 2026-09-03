app_name = "it_book"
app_title = "IT Book"
app_publisher = "Norwa IT Department"
app_description = "IT department project, maintenance, asset, incident, backup, and reporting register"
app_email = "it@example.com"
app_license = "MIT"

fixtures = [
    {"dt": "Role", "filters": [["role_name", "in", ["IT Manager", "IT Officer", "Department Head", "IT Auditor"]]]},
    {"dt": "Number Card", "filters": [["module", "=", "IT Book"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "IT Book"]]},
    {"dt": "Workspace", "filters": [["module", "=", "IT Book"]]},
    {"dt": "Report", "filters": [["module", "=", "IT Book"]]},
    {"dt": "IT Checklist Template"},
]

scheduler_events = {
    "daily": [
        "it_book.reporting.summary.send_daily_summary",
        "it_book.reporting.summary.flag_overdue_and_unrealistic_records",
    ],
    "weekly": [
        "it_book.reporting.summary.send_weekly_summary",
    ],
}

doctype_js = {
    "IT Project": "public/js/it_project.js",
}

after_install = "it_book.install.after_install.create_default_records"
