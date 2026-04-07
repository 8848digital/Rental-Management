// Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Warning Letter", {
	// refresh(frm) {

	// },

    setup: function(frm) {
        frm.set_query("employee", function() {
            return {
                filters: {
                    status: "Active"
                }
            };
        });
        frm.set_query("hr_manager", function() {
            return {
                query: "frappe.core.doctype.user.user.user_query",
                filters: {
                    role: "HR Manager"
                }
            };
        });

        frm.set_query("warning_template", function() {
            return {
                filters: {
                    title: frm.doc.title
                }
            };
        });

    },

    title: function(frm) {
        frm.set_value("warning_template", "");

        frm.set_query("warning_template", function() {
            return {
                filters: {
                    title: frm.doc.title
                }
            };
        });

    }

});
