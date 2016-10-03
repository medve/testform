#-*-encoding:utf-8-*-
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class PhoneApproveGenerator(PasswordResetTokenGenerator):
	phone = ""
	#нечень красиво пропатчим стандартный генератор
	#токенов для сброса паролей

	def make_token(self, user, phone):
		self.phone = phone
		return super(PhoneApproveGenerator, self).make_token(self, user)

	def check_token(self, user, phone, token):
		self.phone = phone
		return super(PhoneApproveGenerator, self).check_token(self, user, token)

	def _make_hash_value(self, user, timestamp):
        # Ensure results are consistent across DB backends
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
            six.text_type(user.pk) + user.password +
            six.text_type(login_timestamp) + six.text_type(timestamp) 
            + six.text_type(self.phone)
        )

token_generator = PhoneApproveGenerator()