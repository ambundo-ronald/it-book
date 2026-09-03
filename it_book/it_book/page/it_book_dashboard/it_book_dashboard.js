frappe.pages["it-book-dashboard"].on_page_load = function (wrapper) {
  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: __("IT Book Dashboard"),
    single_column: true,
  });

  page.set_primary_action(__("Refresh"), () => load_dashboard(page), "refresh");
  $(page.body).addClass("it-book-dashboard");
  load_dashboard(page);
};

async function load_dashboard(page) {
  $(page.body).html(`<div class="it-book-loading">${__("Loading dashboard...")}</div>`);

  const [summaryResponse, alertsResponse, dueResponse, activityResponse] = await Promise.all([
    frappe.call("it_book.reporting.api.dashboard_summary"),
    frappe.call("it_book.reporting.api.open_alerts"),
    frappe.call("it_book.reporting.api.upcoming_due_dates", { days: 14 }),
    frappe.call("it_book.reporting.api.recent_activity", { limit: 10 }),
  ]);

  const summary = summaryResponse.message || {};
  const alerts = alertsResponse.message || {};
  const due = dueResponse.message || {};
  const activity = activityResponse.message || {};

  $(page.body).html(`
    <div class="it-book-grid">
      ${metric_card(__("Open Projects"), summary.projects_open, __("of {0} total", [summary.projects_total || 0]))}
      ${metric_card(__("Projects At Risk"), summary.projects_at_risk, __("Average progress {0}%", [summary.average_progress || 0]))}
      ${metric_card(__("Open Incidents"), summary.open_incidents, __("Critical {0}", [summary.critical_incidents || 0]))}
      ${metric_card(__("Backup Warnings"), summary.backup_warnings_7d, __("Last 7 days"))}
      ${metric_card(__("Budget Use"), `${summary.budget_utilization || 0}%`, __("Actual vs planned"))}
      ${metric_card(__("Asset Returns"), summary.overdue_asset_returns, __("Overdue"))}
    </div>

    <div class="it-book-sections">
      ${section(__("Open Alerts"), render_alerts(alerts))}
      ${section(__("Upcoming Due Dates"), render_due_dates(due))}
      ${section(__("Recent Activity"), render_recent_activity(activity))}
    </div>
  `);
}

function metric_card(label, value, hint) {
  return `
    <div class="it-book-metric">
      <div class="it-book-metric-label">${frappe.utils.escape_html(label)}</div>
      <div class="it-book-metric-value">${frappe.utils.escape_html(value ?? 0)}</div>
      <div class="it-book-metric-hint">${frappe.utils.escape_html(hint || "")}</div>
    </div>
  `;
}

function section(title, body) {
  return `
    <div class="it-book-section">
      <h3>${frappe.utils.escape_html(title)}</h3>
      ${body}
    </div>
  `;
}

function render_alerts(alerts) {
  const rows = [
    ...(alerts.overdue_projects || []).map((row) => [__("Project"), row.project_title, row.due_date]),
    ...(alerts.failed_backups || []).map((row) => [__("Backup"), `${row.system_name}: ${row.status}`, row.backup_date]),
    ...(alerts.critical_incidents || []).map((row) => [__("Incident"), row.incident_title, row.reported_on]),
    ...(alerts.overdue_asset_returns || []).map((row) => [__("Asset"), `${row.asset}: ${row.to_person || ""}`, row.expected_return_date]),
  ];
  return render_table([__("Type"), __("Detail"), __("Date")], rows);
}

function render_due_dates(due) {
  const rows = [
    ...(due.projects || []).map((row) => [__("Project"), row.project_title, row.due_date]),
    ...(due.maintenance || []).map((row) => [__("Maintenance"), row.maintenance_title, row.scheduled_date]),
    ...(due.checklists || []).map((row) => [__("Checklist"), row.subject, row.due_date]),
  ];
  return render_table([__("Type"), __("Detail"), __("Due Date")], rows);
}

function render_recent_activity(activity) {
  const rows = [
    ...(activity.activities || []).map((row) => [__("Activity"), row.activity_title, row.activity_date]),
    ...(activity.incidents || []).map((row) => [__("Incident"), row.incident_title, row.reported_on]),
    ...(activity.changes || []).map((row) => [__("Change"), row.change_title, row.planned_release_date]),
  ];
  return render_table([__("Type"), __("Detail"), __("Date")], rows);
}

function render_table(headers, rows) {
  if (!rows.length) {
    return `<div class="text-muted">${__("No records found")}</div>`;
  }

  return `
    <div class="table-responsive">
      <table class="table table-sm table-bordered">
        <thead>
          <tr>${headers.map((header) => `<th>${frappe.utils.escape_html(header)}</th>`).join("")}</tr>
        </thead>
        <tbody>
          ${rows
            .map(
              (row) => `
                <tr>${row.map((cell) => `<td>${frappe.utils.escape_html(cell || "")}</td>`).join("")}</tr>
              `
            )
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}
