// Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Settlement', {
    date_of_settlement:function(frm) {
        fetch_ticket_allowance(frm);
    },
    type_of_settlement: function(frm) {
        fetch_ticket_allowance(frm);
    },
    employee: function(frm) {
        fetch_ticket_allowance(frm);
        if (!frm.doc.employee) return;

        frappe.db.get_doc('Employee', frm.doc.employee).then(emp => {

            let monthly_salary =
                flt(emp.custom_basic) +
                flt(emp.custom_food_allowances_fa) +
                flt(emp.custom_house_rent_allowances) +
                flt(emp.custom_other_allowances) +
                flt(emp.custom_transporatation_allowances);

            frm.set_value("monthly_salary", monthly_salary);
        });


        if (!frm.doc.employee || !frm.doc.date_of_settlement) return;

        const allowed_types = [
            "Vacation Settlement",
            "Final Settlement",
            "Internal Transfer Settlement"
        ];

        if (!allowed_types.includes(frm.doc.type_of_settlement)) return;

        frappe.call({
            method: "rental_management.rental_management.doctype.leave_settlement.leave_settlement.get_ticket_allowance",
            args: {
                employee: frm.doc.employee,
                settlement_date: frm.doc.date_of_settlement
            },
            callback: function(r) {

                if (!r.message) return;

                frm.clear_table("ticket_allowance");

                r.message.forEach(row => {
                    let d = frm.add_child("ticket_allowance");

                    d.from = row.from;
                    d.to = row.to;
                    d.amount = row.amount;
                });

                frm.refresh_field("ticket_allowance");
            }
        });

    },
    last_working_day: function(frm) {
        calculate_total_service(frm);
    },

    doj__re_joining_date: function(frm) {
        calculate_total_service(frm);
    },
    validate: function(frm) {

        let total_entitlements = 0;
        let total_deductions = 0;

        function sum_table(table){
            let total = 0;
            (table || []).forEach(row=>{
                total += flt(row.amount);
            });
            return total;
        }

        // Child table totals
        total_entitlements += sum_table(frm.doc.salary_due);
        total_entitlements += sum_table(frm.doc.leave_pay);
        total_entitlements += sum_table(frm.doc.gratuity_pay);
        total_entitlements += sum_table(frm.doc.ticket_allowance);

        // Add allowances from parent fields
        total_entitlements += flt(frm.doc.overtime_allowance);
        total_entitlements += flt(frm.doc.other_allowance);

        // Deductions
        total_deductions += flt(frm.doc.outstanding_advance);
        total_deductions += flt(frm.doc.traffic_fine);
        total_deductions += flt(frm.doc.adjustments);
        total_deductions += flt(frm.doc.other_deduction);

        // Set values
        frm.set_value("total_entitlements", total_entitlements);
        frm.set_value("total_deductions", total_deductions);
        frm.set_value("total_settlement_payable", total_entitlements - total_deductions);
    }
});

function calculate_total_service(frm) {

    if(frm.doc.last_working_day && frm.doc.doj__re_joining_date){

        let start = frappe.datetime.str_to_obj(frm.doc.doj__re_joining_date);
        let end = frappe.datetime.str_to_obj(frm.doc.last_working_day);

        let diff_days = frappe.datetime.get_day_diff(end, start);

        let total_service = (diff_days / 30).toFixed(1);

        frm.set_value("total_service", total_service);
    }
}
frappe.ui.form.on('Salary Due', {
    from: function(frm, cdt, cdn) {
        calculate_row(frm, cdt, cdn);
    },
    to: function(frm, cdt, cdn) {
        calculate_row(frm, cdt, cdn);
    }
});

frappe.ui.form.on('Leave Pay', {
    from: function(frm, cdt, cdn) {
        calculate_row(frm, cdt, cdn);
    },
    to: function(frm, cdt, cdn) {
        calculate_row(frm, cdt, cdn);
    }
});

frappe.ui.form.on('Ticket Allowance', {
    from: function(frm, cdt, cdn) {
        calculate_row(frm, cdt, cdn);
    },
    to: function(frm, cdt, cdn) {
        calculate_row(frm, cdt, cdn);
    }
});

frappe.ui.form.on('Gratuity Pay', {
    from: function(frm, cdt, cdn) {
        calculate_row(frm, cdt, cdn);
    },
    to: function(frm, cdt, cdn) {
        calculate_row(frm, cdt, cdn);
    }
});

function calculate_row(frm, cdt, cdn){

    let row = locals[cdt][cdn];

    if(row.from && row.to){

        // calculate duration
        let duration = frappe.datetime.get_day_diff(row.to, row.from) + 1;

        if("days" in row){
            frappe.model.set_value(cdt, cdn, "days", duration);
        }
        if("tenure" in row){
            frappe.model.set_value(cdt, cdn, "tenure", duration);
        }

        // get days in month
        let d = new Date(row.from);
        let month_days = new Date(d.getFullYear(), d.getMonth()+1, 0).getDate();

        // calculate amount
        let amount = (flt(frm.doc.monthly_salary) / month_days) * duration;

        frappe.model.set_value(cdt, cdn, "amount", amount);
    }
}

function fetch_ticket_allowance(frm) {

    if (!frm.doc.employee || !frm.doc.date_of_settlement) return;

    const allowed_types = [
        "Vacation Settlement",
        "Final Settlement",
        "Internal Transfer Settlement"
    ];

    if (!allowed_types.includes(frm.doc.type_of_settlement)) return;

    frappe.call({

        method: "rental_management.rental_management.doctype.leave_settlement.leave_settlement.get_ticket_allowance",

        args: {
            employee: frm.doc.employee,
            settlement_date: frm.doc.date_of_settlement
        },

        callback: function(r) {

            if (!r.message) return;

            frm.clear_table("ticket_allowance");

            r.message.forEach(row => {

                let d = frm.add_child("ticket_allowance");

                d.from = row.from;
                d.to = row.to;
                d.amount = row.amount;

            });

            frm.refresh_field("ticket_allowance");

        }

    });

}