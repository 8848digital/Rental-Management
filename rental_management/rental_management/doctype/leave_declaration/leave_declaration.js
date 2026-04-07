// Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("LEAVE DECLARATION", {
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
    }
});
