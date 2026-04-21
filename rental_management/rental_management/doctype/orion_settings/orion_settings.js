// Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Orion Settings", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Ticket Entitlement', {
    designation_selector: function(frm, cdt, cdn) {

        let row = locals[cdt][cdn];

        // get already selected designations
        let existing = [];
        if (row.designations) {
            existing = row.designations.split(',').map(d => d.trim());
        }

        const dialog = new frappe.ui.Dialog({
            title: "Select Designations",
            fields: [
                {
                    fieldname: "designations",
                    label: "Designations",
                    fieldtype: "MultiSelectList",
                    get_data: function(txt) {
                        return frappe.db.get_link_options("Designation", txt);
                    },
                    default: existing
                }
            ],
            primary_action_label: "Set",
            primary_action(values) {

                let selected = values.designations || [];

                // merge previous + new
                let merged = Array.from(new Set([...existing, ...selected]));

                frappe.model.set_value(
                    cdt,
                    cdn,
                    "designations",
                    merged.join(", ")
                );

                dialog.hide();
            }
        });

        dialog.show();
    }
});