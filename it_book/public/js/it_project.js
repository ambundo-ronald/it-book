frappe.ui.form.on("IT Project", {
  planned_budget(frm) {
    set_budget_utilization(frm);
  },
  actual_spend(frm) {
    set_budget_utilization(frm);
  },
  progress(frm) {
    if ((frm.doc.progress || 0) > 100) {
      frm.set_value("alert_status", "Unrealistic Report");
    }
  },
});

function set_budget_utilization(frm) {
  const planned = frm.doc.planned_budget || 0;
  const actual = frm.doc.actual_spend || 0;
  frm.set_value("budget_utilization", planned ? (actual / planned) * 100 : 0);
}
