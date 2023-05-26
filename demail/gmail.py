
import os
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
    
    if to_email_addresses==None and cc_email_addresses==None and bcc_email_addresses==None:
        raise Exception('No email addresses specified')
    
    if to_email_addresses is not None:
        to_email_addresses = to_email_addresses.split(',')
    if cc_email_addresses is not None:
        cc_email_addresses = cc_email_addresses.split(',')
    if bcc_email_addresses is not None:
        bcc_email_addresses = bcc_email_addresses.split(',')

    if body.__class__ == list:
        for ele in range(len(body)):
            if os.path.exists(body[ele]):
                body[ele] = yagmail.inline(body[ele])

    yag = yagmail.SMTP(user=user, password=password)
    yag.send(to=to_email_addresses
             , subject=subject
             , contents=body
             , attachments=attach_file_address
             , cc=cc_email_addresses
             , bcc=bcc_email_addresses)