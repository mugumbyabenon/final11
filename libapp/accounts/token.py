from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from .models import User
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(User.username) + text_type(timestamp)
        )
generate_token = TokenGenerator()
