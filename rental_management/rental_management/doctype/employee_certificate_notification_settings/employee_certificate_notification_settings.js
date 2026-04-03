// Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Employee Certificate Notification Settings", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Employee Certificate Notification Settings", {
    refresh(frm) {

        // Filter Role
        frm.fields_dict.employee_certificate_notification_detail.grid.get_field("role").get_query = function () {
            return {
                filters: {
                    disabled: 0
                }
            };
        };

        // Filter Sender
        frm.fields_dict.employee_certificate_notification_detail.grid.get_field("sender").get_query = function () {
            return {
                filters: {
                    enable_outgoing: 1
                }
            };
        };

    }
});