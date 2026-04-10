frappe.ui.form.on('Employee', {

    final_confirmation_date(frm) {
        calculate_probation(frm);
    },

    custom_probation_period(frm) {
        calculate_probation(frm);
    }

});

function calculate_probation(frm) {

    if (frm.doc.final_confirmation_date && frm.doc.custom_probation_period) {

        let end_date = frappe.datetime.add_days(
            frm.doc.final_confirmation_date,
            frm.doc.custom_probation_period
        );

        frm.set_value("custom_probation_end_date", end_date);
    }

}