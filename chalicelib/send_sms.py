from chalicelib import config
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging


def send_cust_sms_absolute(cust_phone, cust_message):
    """
    This function sends an SMS using Twilio. Refer to Twilio's documentation to get started.
    :param cust_phone: The phone number to send the SMS to. This should be in E.164 format. Example: +15551234567
    :param cust_message: The SMS message as a string.
    """

    twilio_account_sid = config.twilio_account_sid
    twilio_auth_token = config.twilio_auth_token
    twilio_from_number = config.twilio_from_number

    client = Client(twilio_account_sid, twilio_auth_token)
    try:
        message = client.messages.create(
            body=cust_message,
            from_=twilio_from_number,
            to=cust_phone
        )
    except TwilioRestException as e:
        logging.error(f'An error occurred sending a message with Twilio: {e}')


