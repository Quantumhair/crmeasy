import stripe

from django.conf import settings

def process_payment(request, email, fee):
    # Set your secret key: remember to change this to your live secret key
    # in production. See your keys here https://manage.stripe.com/account
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # Create a Customer
    stripe_customer = stripe.Customer.create(
        card=token,
        description=email
    )

    # Charge the Customer instead of the card
    stripe.Charge.create(
        amount=fee, # in cents
        currency="usd",
        customer=stripe_customer.id
    )

    return stripe_customer
