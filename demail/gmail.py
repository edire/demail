
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def CleanEmailList(email_list):
    final_list = []
    if email_list is not None:
        email_list = email_list.split(',')
        for e in email_list:
            e = e.strip()
            if(re.fullmatch(regex, e)):
                final_list.append(e)
    # if final_list == []:
    #     final_list = None
    return final_list


def SendEmail(to_email_addresses
              , subject
              , body
              , attach_file_address=None
              , cc_email_addresses=None
              , bcc_email_addresses=None
              , user=os.getenv('EMAIL_UID')
              , password=os.getenv('EMAIL_PWD')
              ):

    to_email_addresses = CleanEmailList(to_email_addresses)
    cc_email_addresses = CleanEmailList(cc_email_addresses)
    bcc_email_addresses = CleanEmailList(bcc_email_addresses)
    all_email_addresses = to_email_addresses + cc_email_addresses + bcc_email_addresses
    if type(attach_file_address) == str:
        attach_file_address = [attach_file_address]

    if to_email_addresses==None and cc_email_addresses==None and bcc_email_addresses==None:
        raise Exception('No valid email addresses specified')

    message = MIMEMultipart()
    message["To"] = ", ".join(to_email_addresses)
    message["Cc"] = ", ".join(cc_email_addresses)
    message["From"] = user
    message["Subject"] = subject

    # Add body to email
    html_string = ""
    for x in body:
        if os.path.exists(x):
            attach_file_address.append(x)
            file_name = os.path.basename(x)
            file_extension = file_name.split('.')[-1]
            image_name = file_name[:len(file_name)-len(file_extension)-1]
            html_string += f'<img src="cid:{image_name}">'
        elif x == "":
            html_string += "<br>"
        else:
            html_string += f"<p>{x}</p>"
        html_string += "\n"


    html_content = f"""
    <html>
    <body>
        {html_string}
    </body>
    </html>
    """
    message.attach(MIMEText(html_content, "html"))

    # Add attachment to email
    if attach_file_address:
        for file_path in attach_file_address:
            with open(file_path, "rb") as file:
                file_name = os.path.basename(file_path)
                file_extension = file_name.split('.')[-1]
                image_name = file_name[:len(file_name)-len(file_extension)-1]
                if file_extension in ['jpeg', 'png', 'jpg', 'gif']:
                    attachment = MIMEImage(file.read())
                    attachment.add_header('Content-ID', f'<{image_name}>')
                    attachment.add_header('Content-Disposition', 'inline', filename=file_name)
                else:
                    attachment = MIMEApplication(file.read(), _subtype=file_extension)
                    attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
                message.attach(attachment)


    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(user, password)
        server.sendmail(
            user,
            all_email_addresses,
            message.as_string()
        )



############################################################################################################

# import yagmail


# def SendEmail(to_email_addresses
#               , subject
#               , body
#               , attach_file_address=None
#               , cc_email_addresses=None
#               , bcc_email_addresses=None
#               , user=os.getenv('yagmail_user')
#               , password=os.getenv('yagmail_password')
#               ):
    

#     if body.__class__ == list:
#         for ele in range(len(body)):
#             if os.path.exists(body[ele]):
#                 body[ele] = yagmail.inline(body[ele])

#     yag = yagmail.SMTP(user=user, password=password)
#     yag.send(to=to_email_addresses
#              , subject=subject
#              , contents=body
#              , attachments=attach_file_address
#              , cc=cc_email_addresses
#              , bcc=bcc_email_addresses)