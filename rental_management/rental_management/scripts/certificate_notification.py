import frappe
from frappe.utils import today, date_diff


def certificate_expiry_notification():
    """
    Scheduled job to send email notifications for employee certificate expiry.

    This function:
    - Reads notification configurations from 'Employee Certificate Notification Settings'.
    - Checks each employee's certificates for expiry dates.
    - Sends email notifications when the remaining days match the configured notification days.
    """

    settings = frappe.get_single("Employee Certificate Notification Settings")

    employees = frappe.get_all("Employee", fields=["name", "user_id"])

    # Track notifications already sent to employees to avoid duplicates
    sent_employee_notifications = set()

    for config in settings.employee_certificate_notification_detail:

        notify_days = config.notify_before_days

        # Fetch role users once per config
        role_recipients = get_users_by_role(config.role)

        for emp in employees:

            emp_doc = frappe.get_doc("Employee", emp.name)

            for cert in emp_doc.custom_certificates:

                expiry_date = cert.get(config.field_notification_based_on)

                if not expiry_date:
                    continue

                days_left = date_diff(expiry_date, today())

                if days_left != notify_days:
                    continue

                context = {"doc": cert}

                subject = frappe.render_template(config.subject, context)
                message = frappe.render_template(config.message, context)

                recipients = list(role_recipients)

                # Send email to employee if enabled
                if config.trigger_email_to_employee and emp_doc.user_id:

                    key = (emp_doc.name, cert.certification_name)

                    if key not in sent_employee_notifications:
                        recipients.append(emp_doc.user_id)
                        sent_employee_notifications.add(key)

                frappe.sendmail(
                    recipients=list(set(recipients)),
                    subject=subject,
                    message=message,
                    sender=config.sender_email
                )


def get_users_by_role(role_name):
    """
    Fetch email IDs of enabled users assigned to a specific role.
    """

    users = frappe.get_all(
        "Has Role",
        filters={"role": role_name},
        pluck="parent"
    )

    if not users:
        return []

    emails = frappe.get_all(
        "User",
        filters={
            "name": ["in", users],
            "enabled": 1
        },
        pluck="email"
    )

    return list(set(emails))