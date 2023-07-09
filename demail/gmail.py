
import os
import yagmail
import re


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def CleanEmailList(email_list):
    final_list = []
    if email_list is not None:
        email_list = email_list.split(',')
        for e in email_list:
            e = e.strip()
            if(re.fullmatch(regex, e)):
                final_list.append(e)
    if final_list == []:
        final_list = None
    return final_list


def SendEmail(to_email_addresses
              , subject
              , body
              , attach_file_address=None
              , cc_email_addresses=None
              , bcc_email_addresses=None
              , user=os.getenv('yagmail_user')
              , password=os.getenv('yagmail_password')
              ):
    
    to_email_addresses = CleanEmailList(to_email_addresses)
    cc_email_addresses = CleanEmailList(cc_email_addresses)
    bcc_email_addresses = CleanEmailList(bcc_email_addresses)

    if to_email_addresses==None and cc_email_addresses==None and bcc_email_addresses==None:
        raise Exception('No valid email addresses specified')

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