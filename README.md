# stripe-webhook-lambda-easy
 An easily configurable Stripe.com webhook handler for AWS Lambda, deployed via Chalice.

It's designed to be easy to configure and easy to deploy. It's also designed to be easy to extend with additional
functionality. It has built in examples for handling common webhooks as well as the ability to interface with Twilio and
Twilio Sendgrid to send SMS and email notifications. The code is commented and should be easy to follow. If you don't
want to use the Twilio functionality, you can easily remove it.

Lambda is a great way to handle webhooks because it's cheap and easy to scale. It can handle almost any rate of webhooks
from small business to enterprise, and for most small businesses it's free. Check out AWS's free tier for more information.

## Pre-requisites
- An AWS account
- A Stripe account
- A Twilio account (optional)
- A Twilio Sendgrid account (optional)
- Python 3.9 (AWS supports 3.9 for Chalice deployment to Lambda)

## 1. Configuration

Configuration of the program is done through three config files. The first is the `config.json` file. This file
will allow you to access to the Chalice configuration options. See the [Chalice documentation](https://chalice.readthedocs.io/en/latest/topics/configfile.html).

The second file is the AWS config file. It's in the folder .AWS. Set your region in this file. 
See the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for more information.

The third file is the Stripe and Twilio config. This is the config.py found in chalicelib. This file contains
the Stripe and Twilio API keys, as well as the Twilio phone number and Twilio Sendgrid email address. You will need to
refer to the Twilio and Stripe documentation to get these keys. I HIGHLY recommend not hard coding them, and instead
using a solution like Parameter Store or Secrets Manager to hold these keys. If you do so, remember to update 
your Lambda function's IAM Role to allow access to the keys.

## 2. Edit the code

The main app.py file contains all of the webhook code. You'll need to read through it, and edit it to fit your needs.
I've provided numerous examples of how to access simple customer information through the webhooks and how to send SMS
and emails by calling their functions. You can also add your own functions to the code and call them. You can add new
webhook handlers by adding the `elif` statement to the end prior to the `else` statement. See the Stripe docs for a
list of all the webhooks that can be sent here: [Stripe Events](https://stripe.com/docs/api/events/types).

## 3. Deployment

Deployment to AWS is completed through Chalice from the command line. Configure your environmental variables with your
AWS credentials prior to deployment. Refer to the [AWS CLI documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
for more information. It is possible to deploy this without Chalice using Lambda's GUI.

Simply enter the following command while navigated to the base directory containing the app.py file:

    chalice deploy

## 4. Testing

After it is deployed you will get your API endpoint. Make sure to add the app route to the end, for example:

    https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/api/webhook

You can then test it with Stripe's excellent CLI. You can find the CLI here: [Stripe CLI](https://stripe.com/docs/stripe-cli).

Then follow Stripe's instructions to test the webhook. The instructions are here: [Stripe Webhook Testing](https://stripe.com/docs/webhooks/test).

When you set the `forward_to` parameter, you can set it to your Lambda endpoint instead of a local server as it suggests. This will allow
you to send the `trigger` tests to your actual Lambda function.

## 5. Going live

All you need to do to set it live, after you've done your testing, is to go to the Stripe dashboard and set the webhook
endpoint to your Lambda endpoint. The instructions are here: [Stripe Webhook Dashboard](https://stripe.com/docs/webhooks/go-live).

## 6. Extending the code

If you want to add extensions to the code, you can do so by adding your own functions in an additional .py file placed in the chalicelib folder,
and called in the app.py file. You will then need to redeploy the code via `chalice deploy`.
