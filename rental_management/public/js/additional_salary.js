
frappe.ui.form.on('Additional Salary', {
    // refresh: function(frm) {
    //     trigger_fetch(frm);
    // },
    // Trigger on payroll date change
    payroll_date: function(frm) {
        trigger_fetch(frm);
    },

    // Trigger when salary component changes
    salary_component: function(frm) {
        trigger_fetch(frm);
    },

    // Trigger when from_date changes
    from_date: function(frm) {
        trigger_fetch(frm);
    },

    // Trigger when to_date changes
    to_date: function(frm) {
        trigger_fetch(frm);
    },

    // Trigger when employee changes
    employee: function(frm) {
        trigger_fetch(frm);
    }
});


function trigger_fetch(frm) {

    if (!frm.doc.employee || frm.doc.salary_component !== "Total Deduction") {
        return;
    }

    if (!frm.doc.payroll_date && !(frm.doc.from_date && frm.doc.to_date)) {
        frm.clear_table("penalties_details");
        frm.set_value("amount", 0);
        frm.refresh_field("penalties_details");
        return;
    }

    fetch_deduction(frm);
}


function fetch_deduction(frm) {

    let method = "";
    let args = { employee: frm.doc.employee };

    // Decide API based on available filters
    if (frm.doc.payroll_date && !frm.doc.is_recurring) {
        method = "rental_management.rental_management.doctype.additional_salary.get_deduction_by_payroll_date";
        args.payroll_date = frm.doc.payroll_date;
    } else {
        method = "rental_management.rental_management.doctype.additional_salary.get_deduction_by_date_range";
        args.from_date = frm.doc.from_date;
        args.to_date = frm.doc.to_date;
    }

    frappe.call({
        method: method,
        args: args,
        callback: function(r) {

            // Clear existing rows before adding new ones
            frm.clear_table("custom_penalties_detail");
            if (r.message && r.message.rows) {

                r.message.rows.forEach(d => {

                    let row = frm.add_child("custom_penalties_detail");

                    // Map response fields to child table
                    row.penalty_name = d.type_of_penalty;
                    row.employee_deduction_reference = d.name;
                    row.remaining_amount = d.remaining_amount;
                    row.date_of_deduction_occurred = d.deduction_date;
                    row.remarks=d.remarks
                    // Ensure installment does not exceed remaining
                    if (d.installment_amount > d.remaining_amount) {
                        row.installation_amount = d.remaining_amount;
                    } else {
                        row.installation_amount = d.installment_amount;
                    }
                });

                frm.refresh_field("custom_penalties_detail");
                calculate_total(frm);
            }
        }
    });
}

frappe.ui.form.on("Penalties Details", {

    installation_amount: function(frm, cdt, cdn) {

        let row = locals[cdt][cdn];

        // Prevent negative values
        if (row.installation_amount < 0) {
            frappe.msgprint("Amount cannot be negative");
            row.installation_amount = 0;
        }

        // Prevent exceeding remaining amount
        if (row.installation_amount > row.remaining_amount) {
            frappe.msgprint("Amount cannot exceed remaining amount");
            row.installation_amount = row.remaining_amount;
        }

        // Recalculate total after change
        calculate_total(frm);
        frm.refresh_field("custom_penalties_detail");
    }
});



function calculate_total(frm) {

    let total = 0;

    (frm.doc.custom_penalties_detail || []).forEach(row => {
        total += flt(row.installation_amount);
    });

    // Set total to parent field
    frm.set_value("amount", total);
}