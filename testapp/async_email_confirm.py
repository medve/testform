from __future__ import absolute_import

from .tasks import send_email_async
from .token import token_generator

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode


'''
Содержит функции для подтверждения email или телефона
'''

def send_confirm_email(user,phone, token_generator = default_token_generator,
                            from_email, use_https = False,
                            subject_template_name='subject_template.txt',
                            email_template_name='email_template.html',
                            html_email_template_name = None,
                            extra_email_context = None):
        context = {
                'email': user.email,
                'phone': phone.phone,
                'phone_id': phone.id,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user, phone.phone),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
           send_mail_async.delay(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)