
import os
import sendgrid
import sendgrid.helpers.mail as sgm
import base64


def SendEmail(to_email_addresses
              , subject
              , body
              , body_html=None
              , attach_file_address=None
              , cc_email_addresses=None
              , bcc_email_addresses=None
              , from_email = os.getenv('email_from')
              , reply_to = os.getenv('email_reply_to')
              ):
              
    mail = sgm.Mail(from_email=from_email
                    , to_emails=to_email_addresses
                    , subject=subject
                    , plain_text_content=body
                    , html_content=body_html
                    )
    mail.reply_to = sgm.ReplyTo(reply_to)

    def prep_attachment(attach_file_address):
        with open(attach_file_address, 'rb') as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        attachment = sgm.Attachment()
        attachment.file_content = sgm.FileContent(encoded)
        if attach_file_address[-4:].lower() in ['jpeg', '.png', '.jpg', '.gif']:
            attachment.file_type = sgm.FileType("image/jpeg")
        else:
            attachment.file_type = sgm.FileType("application/pdf")
        attachment.file_name = sgm.FileName(os.path.basename(attach_file_address))
        attachment.disposition = sgm.Disposition("attachment")
        return attachment

    if attach_file_address != None:
        if type(attach_file_address) != list:
            attach_file_address = [attach_file_address]
        for file_address in attach_file_address:
            attachment = prep_attachment(file_address)
            mail.add_attachment(attachment)

    if cc_email_addresses != None:
        for email_address in cc_email_addresses:
            mail.add_cc(email_address)

    if bcc_email_addresses != None:
        for email_address in bcc_email_addresses:
            mail.add_bcc(email_address)

    # with smtplib.SMTP_SSL('smtp.sendgrid.com', port=465) as smtp:
    #     smtp.login(email_user, email_password)
    #     smtp.send_message(msg)
    sg = sendgrid.SendGridAPIClient(api_key = os.environ.get('SendGridAPIKey'))
    sg.send(mail)