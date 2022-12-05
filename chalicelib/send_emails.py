from chalicelib import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To
import logging


def send_cust_email(cust_name, cust_email, cust_subject, cust_message):
    """
    This function sends an email to a customer using Twilio Sendgrid. Refer to Sendgrid's documentation to get started.
    :param cust_name: Pass the customer's name as a string.
    :param cust_email: Pass the customer's email address as a string.
    :param cust_subject: The email's subject line as a string.
    :param cust_message: The email's message as a string. This string can accept HTML and will be parsed properly by Sendgrid.
    """

    sendgrid_api_key = config.sendgrid_api_key
    sendgrid_from_email = config.sendgrid_from_email
    sendgrid_from_name = config.sendgrid_from_name

    message = Mail(
        from_email=From(
            email=sendgrid_from_email,
            name=sendgrid_from_name
                    ),
        to_emails=To(
            email=cust_email,
            name=cust_name,
                    ),
        subject=cust_subject,
        html_content=cust_message
                )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)

        # You can uncomment the following lines to have the response from Sendgrid SMS messaged to you to make sure your
        # emails are going through.
        # try:
        #     from chalicelib import send_sms
        #     send_sms.send_cust_sms_absolute('+15551234567',
        #                                     f'SendGrid Response: {response.status_code} - {response.body}')
        # except Exception as e:
        #     logging.error(f'An error occurred sending a message with SendGrid and/or Twilio: {e}')

    except Exception as e:
        logging.error(f'An error occurred sending a message with SendGrid: {e}')
