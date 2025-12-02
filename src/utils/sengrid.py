import logging
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from config import settings


class ServiceEmail:
    def __init__(self) -> None:
        self.sg_client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    def send_email(
        self,
        receivers: list[str] | str,
        template_id: str,
        dynamic_data: dict,
        attachments: list[dict] = None
    ) -> dict:

        sg_message = Mail(
            from_email=settings.EMAIL_SENDER,
            to_emails=receivers,
        )

        sg_message.template_id = template_id
        sg_message.dynamic_template_data = dynamic_data

        if attachments:
            for file in attachments:
                encoded = base64.b64encode(file["content"]).decode()
                attach = Attachment(
                    FileContent(encoded),
                    FileName(file["filename"]),
                    FileType(file["type"]),
                    Disposition("attachment")
                )

                sg_message.add_attachment(attach)

        try:
            self.sg_client.send(sg_message)
            logging.info("Mail sent successfully")
        except Exception as e:
            logging.error(f"Failed to send mail: {e}")


sendgrid_service = ServiceEmail()
