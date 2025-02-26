from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
# Use Django's built-in function to generate a token
# This token will be sent in the email's verification link
# https://simpleisbetterthancomplex.com/tutorial/2016/08/24/how-to-create-one-time-link.html

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

generate_email_verification_token = AccountActivationTokenGenerator()