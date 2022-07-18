
import yagmail

def SendEmail(to_email_addresses
              , subject
              , body
              , attach_file_address=None
              , cc_email_addresses=None
              , bcc_email_addresses=None
              , user=os.getenv('yagmail_user')
              , password=os.getenv('yagmail_password')
              ):
    yag = yagmail.SMTP(user=user, password=password)
    yag.send(to=to_email_addresses
             , subject=subject
             , contents=body
             , attachments=attach_file_address
             , cc=cc_email_addresses
             , bcc=bcc_email_addresses)