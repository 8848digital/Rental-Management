from frappe_s3_attachment.frappe_s3_attachment.customization.file.file import CustomFile as S3CustomFile
import frappe

class CustomFile(S3CustomFile):
    
    @property
    def is_remote_file(self):
        frappe.thorw("in")
        if self.file_url and (
            "/api/method/frappe_s3_attachment" in self.file_url
            or self.file_url.startswith(("http://", "https://"))
        ):
            return True
        return super().is_remote_file

    def get_full_path(self):
        frappe.thorw("in")
        if self.file_url and "/api/method/frappe_s3_attachment" in self.file_url:
            return self.file_url
        return super().get_full_path()