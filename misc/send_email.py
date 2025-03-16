"""
Send Email to Dummy Email Address
=============
Sends a email notification if the simulation interupts in-between
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
import datetime

"""
Create a function to connect to smtp Gmail server and send the last error which was
printed in the console
"""
def send_email(subject, body):
    """
    

    Parameters
    ----------
    subject : TYPE
        DESCRIPTION.
    body : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    """
    Enter the dummy email to and from which the email has to been sent
    """
    sender_email = 'dmailthesis@gmail.com'
    sender_password = 'pgfu wrwl peoz vrkp'

    """
    Enter the recipient's email address, in this case same
    """
    recipient_email = 'dmailthesis@gmail.com'

    ######################################
    ##### DONT CHANGE SERVER SETTING #####
    ######################################
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    message = MIMEMultipart()
    message['From'] = "Bearing_Visco_Simulation"
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        """
        Connect to the SMTP sever
        """
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        """
        Send the email and close the connection.
        """
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        
    except Exception as e:
        print(f"Error sending email: {e}")
        print(traceback.format_exc())


# try:
# ##########################    
# # Optimization Looop Here #
# ##########################


# except Exception as e:
#     """
#     Send the error mail
#     """
#     error_subject = f"The simulation has stopped at [INFO {datetime.datetime.now().strftime('%m-%d %H:%M:%S')}] "
#     error_body = f"An error occurred:\n\n{str(e)}\n\n{traceback.format_exc()}"
#     send_email(error_subject, error_body)
