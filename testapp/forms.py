from __future__ import absolute_import

from models import AdditionalPhone
from django import forms
import django.contrib.auth.forms as auth_f
from django.contrib.auth import (
    authenticate, get_user_model
)

from .auth import authenticate_by_phone
import re

from .async_email_confirm import send_confirm_email

from django.forms import BaseInlineFormset
from .token import import token_generator as phone_token_generator

def clean_phone(data):
    return re.match(data,"+\d \d{3} \d{2} \d{2}")

def clean_email(data):
    return re.match(data,
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

User = get_user_model()

class MultiphoneAuthForm(auth_f.AuthentificationForm):
    login_is_phone = False

    def clean_username(self,value):
        if clean_phone(value):
            self.login_is_phone = True
            return value
        elif clean_email(value):
            return value
        raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            if login_is_phone(username):
                self.user_cache = authenticate_by_phone(phone=username,
                                           password=password)
            else:
                self.user_cache = authenticate(email=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

class RegistrationForm(auth_f.UserCreationForm):

    class Meta:
        model = User
        fields = ("email","phone","first_name",
                  "last_name")   

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=True)
        return user


class AdditionalPhoneFormset(BaseInlineFormset):
    from_email = settings.FROM_EMAIL
    phone = forms.CharField(max_length=19)

    def clean(self):
        super(AdditionalPhoneFormset, self).clean()
        for form in self.forms:
            phone = form.cleaned_data["phone"]
            form.cleaned_data["phone"] = self._clean_phone(phone)

    def save_new_objects(self, commit=True):
        new_objects = super(AdditionalPhoneFormset, self).save_new_objects(self, commit=True)
        for phone in new_objects:
            self._activate_phone(user, phone)

    def _clean_phone(self, phone):
        if not clean_phone(phone):
            raise forms.ValidationError("Uncorrect phone number")
        return phone

    def _activate_phone(self, user, phone, use_https = False,
                            email_template_name=None,
                            html_email_template_name = 'email.html'):
        send_confirm_email(user, phone, self.from_email,
                            email_template_name,html_email_template_name)

    class Meta:
        model = AdditionalPhone

AdditionalPhonesFormset = inlineformset_factory(User, AdditionalPhone,
                            fields = ("phone"), can_delete = True)

