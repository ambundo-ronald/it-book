frappe.query_reports["IT Change Register Report"] = {
  filters: [
    {
      fieldname: "change_type",
      label: __("Change Type"),
      fieldtype: "Select",
      options: "\nNew Feature\nEnhancement\nDiscontinued Feature\nConfiguration\nSecurity\nInfrastructure\nEmergency",
    },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: "\nRequested\nImpact Review\nApproved\nIn Progress\nReleased\nRejected\nRolled Back\nDiscontinued",
    },
  ],
};
