frappe.query_reports["IT Asset Register"] = {
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
      options: "\nAvailable\nAssigned\nUnder Repair\nDisposed\nLost\nRetired",
    },
  ],
};
