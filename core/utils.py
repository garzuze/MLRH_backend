from django.contrib.auth.tokens import default_token_generator

# Use Django's built-in function to generate a token
# This token will be sent in the email's verification link
# TODO: go even crazier and make this more secure and don't expose UID on URL

def generate_email_verification_token(user):
    return default_token_generator.make_token(user)
