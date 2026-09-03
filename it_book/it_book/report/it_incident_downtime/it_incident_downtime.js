frappe.query_reports["IT Incident Downtime"] = {
  filters: [
    {
      fieldname: "priority",
      label: __("Priority"),
      fieldtype: "Select",
      options: "\nLow\nMedium\nHigh\nCritical",
    },
    {
      fieldname: "status",
      label: __("Incident Status"),
      fieldtype: "Select",
      options: "\nOpen\nInvestigating\nResolved\nClosed\nCancelled",
    },
  ],
};
