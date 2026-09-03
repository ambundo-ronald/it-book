frappe.query_reports["IT Backup Health"] = {
  filters: [
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: "\nSuccess\nWarning\nFailed\nSkipped",
    },
    {
      fieldname: "days",
      label: __("Last Days"),
      fieldtype: "Int",
      default: 30,
    },
  ],
};
