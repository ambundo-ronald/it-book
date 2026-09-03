frappe.query_reports["IT Project Portfolio"] = {
  filters: [
    {
      fieldname: "department",
      label: __("Department"),
      fieldtype: "Data",
    },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: "\nPlanned\nOngoing\nPending Review\nAt Risk\nCompleted\nCancelled",
    },
  ],
};
