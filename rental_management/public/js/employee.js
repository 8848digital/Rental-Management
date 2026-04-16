frappe.ui.form.on('Employee', {
    // Trigger salary total calculation when any salary component changes
    custom_basic_salary: calculate_total,
    custom_hra: calculate_total,
    custom_ot_allowances: calculate_total,
    custom_food_allowances: calculate_total,
    custom_transportation_allowances: calculate_total,
    
    custom_basic: calculate_total_offered_salary,
    custom_house_rent_allowances: calculate_total_offered_salary,
    custom_food_allowances_fa:calculate_total_offered_salary,
    custom_other_allowances: calculate_total_offered_salary,
    custom_transportation_allowance: calculate_total_offered_salary,
    // Check if the selected designation is marked as Driver
    // If yes, show the Driving Licence field, otherwise hide it
    designation: function(frm) {
        if (frm.doc.designation) {
            frappe.db.get_value(
                "Designation",
                frm.doc.designation,
                "custom_is_driver",
                function(r) {
                    if (r.custom_is_driver) {
                        frm.set_df_property("custom_type_of_driving_licence", "hidden", 0);
                    } else {
                        frm.set_df_property("custom_type_of_driving_licence", "hidden", 1);
                        frm.set_value("custom_type_of_driving_licence", "");
                    }
                }
            );
        }
    },

        setup(frm) {
        calculate_probation(frm);
        calculate_total(frm),
        calculate_total_offered_salary(frm)
        // Loop through all fields available in the Employee form
        Object.keys(frm.fields_dict).forEach(fieldname => {

            // Get the field object from the form
            let field = frm.fields_dict[fieldname];

            // This ensures the logic only applies to fields where options = User
            if (field.df.fieldtype === "Link" && field.df.options === "User") {
                // This replaces the default User search with our custom query
                frm.set_query(fieldname, function () {
                    return {
                        // Employee ID + Employee Name instead of email
                        query: "rental_management.rental_management.doctype.employee.user_by_employee"
                    };
                });

            }

        });


    
        // Ensure driver logic also works on form load
        if (frm.doc.designation) {
            frappe.db.get_value(
                "Designation",
                frm.doc.designation,
                "custom_is_driver",
                function(r) {
                    frm.set_df_property(
                        "custom_type_of_driving_licence",
                        "hidden",
                        r.custom_is_driver ? 0 : 1
                    );
                }
            );
        }
    },

    // Recalculate probation end date when confirmation date changes
    final_confirmation_date(frm) {
        calculate_probation(frm);
    },

    // Recalculate probation end date when probation period changes
    custom_probation_period(frm) {
        calculate_probation(frm);
    }

});


// Calculate Probation End Date = Confirmation Date + Probation Period
function calculate_probation(frm) {

    if (frm.doc.final_confirmation_date && frm.doc.custom_probation_period) {

        let end_date = frappe.datetime.add_months(
            frm.doc.final_confirmation_date,
            frm.doc.custom_probation_period
        );

        frm.set_value("custom_probation_end_date", end_date);
    }
}


// Calculate Total Salary by summing all salary components
function calculate_total(frm) {

    let total =
        (parseInt(frm.doc.custom_basic_salary) || 0) +
        (parseInt(frm.doc.custom_hra) || 0) +
        (parseInt(frm.doc.custom_ot_allowances) || 0) +
        (parseInt(frm.doc.custom_food_allowances) || 0) +
        (parseInt(frm.doc.custom_transportation_allowances) || 0);

    // Set calculated value in Total Salary field
    frm.set_value("custom_total_salary", total);
}

function calculate_total_offered_salary(frm) {

    let total =
        (parseInt(frm.doc.custom_basic) || 0) +
        (parseInt(frm.doc.custom_house_rent_allowances) || 0) +
        (parseInt(frm.doc.custom_other_allowances) || 0) +
        (parseInt(frm.doc.custom_food_allowances_fa) || 0) +
        (parseInt(frm.doc.custom_transportation_allowance) || 0);

    // Set calculated value in Total Salary field
    frm.set_value("custom_total_salary_as_per_offer_letter", total);
}