import stripe
from chalice import Chalice
from logging import error, warning, info, basicConfig, INFO
from chalicelib.send_emails import send_cust_email
from chalicelib.send_sms import send_cust_sms_absolute
from chalicelib import config

# Change the below to your app name, and you can disable the debug logging.
app = Chalice(app_name='stripe-webhook-lambda-easy')
app.debug = True

# You can also add the Stripe API key into this file, but it's better to use the config to
# access it from AWS Parameter Store or Secrets Manager.
# stripe.api_key = ''

# These are the JSON returns to Stripe from the webhook. Stripe expects a response, so if you don't return a
# response, Stripe will keep trying to send the webhook until it gets a response.
no_success = '{"success": false}'
yes_success = '{"success": true}'


# This is the endpoint that Stripe will call when a webhook is sent. There is a procedure to go through to validate that
# the webhook is coming from Stripe. I have removed this procedure because this file does not provision customer
# resources or do anything besides send messages. If you want to provision resources or do anything money related then
# it's advisable to add the functionality. I didn't need it, and it sometimes causes errors, so I removed it. You can
# get a template from Stripe and read about it here: https://stripe.com/docs/webhooks/signatures
@app.route('/webhook', methods=['POST'])
def webhook():
    # First we load the JSON data from Stripe.
    try:
        event = None
        payload = app.current_request.json_body
        print(f'Payload: {payload}')
        event = payload
    except Exception as e:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return no_success

    # Then we check the type of webhook event it is.
    event_type = event['type']

    # Handle the event

    # Following are some example events and how to access the data in them, and how to call the SMS and Email functions.
    if event_type == 'customer.subscription.deleted':
        try:
            stripe_cust_id = event['data']['object']['customer']
            customer_info = stripe.Customer.retrieve(stripe_cust_id, config.stripe_api_key)
            cust_name = customer_info['name']
            warning(f'Subscription deleted for customer: {stripe_cust_id} - {cust_name}')
            # A potential use for SMS here is to send a message to yourself or the account manager
            # that a subscription was deleted.
            phone_number = '+15551234567'
            message = f'Subscription deleted for customer: {stripe_cust_id} - {cust_name}'
            send_cust_sms_absolute(phone_number, message)
        except Exception as e:
            error(f'⚠️  Webhook error while handling customer.subscription.deleted event: {e}')
        finally:
            return yes_success

    elif event_type == 'charge.failed':
        try:
            stripe_cust_id = event['data']['object']['customer']
            warning(f'Charge failed for customer: {stripe_cust_id}')
            # A potential use here for SMS is to send a message to the customer to let them know their charge has
            # failed, if you've collected their number with Stripe. If you haven't, you can add a call to your own
            # database to grab it.
            customer_info = stripe.Customer.retrieve(stripe_cust_id, config.stripe_api_key)
            cust_name = customer_info['name']
            cust_phone = customer_info['phone']
            message = f'Hi {cust_name}, this is Acme, Inc. We wanted to let you know that your payment has failed. ' \
                      f'Please update your payment information at the billing portal. ' \
                      f'Thank you for being a valued customer!'
            send_cust_sms_absolute(cust_phone, message)
        except Exception as e:
            error(f'⚠️  Webhook error while handling charge.failed event: {e}')
        finally:
            return yes_success

    elif event_type == 'customer.created':
        try:
            # This is an example of how we can handle a new customer being created. This will obviously vary
            # depending on your business, but this is a good example of how to access the data and call the SMS and
            # Email functions.
            stripe_cust_id = event['data']['object']['id']
            customer_info = stripe.Customer.retrieve(stripe_cust_id, config.stripe_api_key)
            cust_email = customer_info['email']
            cust_name = customer_info['name']
            send_cust_email(cust_name, cust_email, "Welcome to Acme, Inc!",
                            f'<p>Welcome to Acme!</p>'
                            f'<p>Thank you for signing up for our service. We are excited to have you on board.</p>'
                            f'<p>Our goal is to provide high quality institutional level trading tools to the '
                            f'retail trader.</p>'
                            f'<p><b>To get you started please reply to this email with your username</b> and we '
                            f'will enable the indicators and algorithms within 24 business hours.</p>'
                            f'<p>You can also join our Discord here to find indicator settings, updates, daily '
                            f'market analysis, and a swing trade bot created with our algorithms that maintains an '
                            f'over 80% win rate: https://discord.gg/your-url</p>'
                            f'<p>You can also reply to this email with any additional questions.</p>'
                            f'<p>Thank you again for signing up and we look forward to working with you!</p>'
                            f'<p>Best,</p>'
                            f'<p>Acme, Inc.</p>')

            cust_phone = customer_info['phone']
            send_cust_sms_absolute(cust_phone, f'Welcome to Acme, Inc! Please check your email for '
                                               f'instructions on how to get started with our institutional grade '
                                               f'indicators and algorithms! If you have any questions or concerns '
                                               f'please send an email to support@acme.com. If you '
                                               f'need to access your billing information please visit '
                                               f'https://billing.stripe.com/p/login/your-portal-url')

            # When a new customer is created we can let ourselves know that we have someone new to reach out to.
            phone_number = '+15551234567'
            message = f'New customer created: {stripe_cust_id} - {cust_name}'
            send_cust_sms_absolute(phone_number, message)
        except Exception as e:
            error(f'⚠️  Webhook error while handling customer.created event: {e}')
        finally:
            return yes_success

    else:
        # Unexpected event type
        error(f'⚠️  Unexpected event type received: {event_type}')
        return yes_success

