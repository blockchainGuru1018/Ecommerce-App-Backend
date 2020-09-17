from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.utils import json
from datetime import datetime, timedelta
import requests
import re
import stripe

from common.exception import CustomException
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    address_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    Zip = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_email': _('Email is invalid or already taken.'),
        'invalid_username': _(
            'Username may only contain alphanumeric characters, and must be no more than 40 characters.'),
        'invalid_name': _('Your full name is required.'),
        'invalid_password': _('Password must have at least 6 characters.'),
        'duplicate_username': _('Username is not available.'),
        'invalid_address_name': _('Address_name field is empty.'),
        'invalid_address': _('Address field is empty.'),
        'invalid_city': _('City field is empty.'),
        'invalid_state': _('State field is empty.'),
        'invalid_Zip': _('Zip field is empty.'),
    }

    class Meta:
        model = User
        fields = ("email", "username", "name", "password", "address_name", "address", "city", "state", "Zip")

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        name = attrs.get("name")
        password = attrs.get("password")
        email_re = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
        address_name = attrs.get("address_name")
        address = attrs.get("address")
        city = attrs.get("city")
        state = attrs.get("state")
        Zip = attrs.get("Zip")

        if not email or not bool(re.match(email_re, email)) or User.objects.filter(email=email).exists():
            raise CustomException(code=11, message=self.error_messages['invalid_email'])
        if username:
            if not bool(re.match('^[a-zA-Z0-9]+$', username)) or len(username) > 40:
                raise CustomException(code=12, message=self.error_messages['invalid_username'])
            elif User.objects.filter(username=username).exists():
                raise CustomException(code=15, message=self.error_messages['duplicate_username'])
        if not name:
            raise CustomException(code=13, message=self.error_messages['invalid_name'])
        if not password or len(password) < 6:
            raise CustomException(code=14, message=self.error_messages['invalid_password'])
        if not address_name:
            raise CustomException(code=16, message=self.error_messages['invalid_address_name'])
        if not address:
            raise CustomException(code=17, message=self.error_messages['invalid_address'])
        if not city:
            raise CustomException(code=18, message=self.error_messages['invalid_city'])
        if not state:
            raise CustomException(code=19, message=self.error_messages['invalid_state'])
        if not Zip:
            raise CustomException(code=20, message=self.error_messages['invalid_Zip'])

        attrs['password'] = make_password(attrs['password'])

        customer = stripe.Customer.create(
            email=email,
            name=name,
        )
        attrs['customer_id'] = customer.id
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    registration_id = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_username': _('Username or email is required.'),
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        registration_id = attrs.get("registration_id")
        if not username:
            raise CustomException(code=10, message=self.error_messages['invalid_username'])

        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            self.user = get_user_model().objects.get(**kwargs)
            if self.user.check_password(password):
                if self.user.is_active:
                    attrs['user'] = self.user
                    return attrs
                else:
                    raise CustomException(code=12, message=self.error_messages['inactive_account'])
        except User.DoesNotExist:
            pass
        raise CustomException(code=11, message=self.error_messages['invalid_credentials'])


class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False)
    provider = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_token': _('Access Token is invalid.'),
        'invalid_provider': _('Google or Facebook login is supported.'),
        'wrong_token': _('wrong google token / this google token is already expired.')
    }

    def validate(self, attrs):
        access_token = attrs.get("access_token")
        provider = attrs.get("provider")

        if not access_token:
            raise CustomException(code=10, message=self.error_messages['invalid_token'])
        if provider not in ["google", "facebook"]:
            raise CustomException(code=11, message=self.error_messages['invalid_provider'])

        if provider == "google":
            payload = {'id_token': access_token}  # validate the token
            r = requests.get('https://oauth2.googleapis.com/tokeninfo', params=payload)
            data = json.loads(r.text)

            if 'error' in data:
                raise CustomException(code=12, message=self.error_messages['wrong_token'])

            attrs['user_info'] = data

        return attrs


class ForgotSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_username': _('Username or email is required.'),
    }

    def validate(self, attrs):
        username = attrs.get("username")
        if not username:
            raise CustomException(code=10, message=self.error_messages['invalid_username'])

        return attrs


class ConfirmTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_token': _('Token is invalid.'),
        'token_expired': _('Reset Token has been expired.'),
        'inactive_account': _('User account is disabled.'),
    }

    def validate(self, attrs):
        token = attrs.get("token")
        if not token or not token.isdigit():
            raise CustomException(code=10, message=self.error_messages['invalid_token'])

        try:
            user = User.objects.get(password_reset_token=int(token))
            if not user.is_active:
                raise CustomException(code=11, message=self.error_messages['inactive_account'])
            if user.password_reset_sent_at.replace(tzinfo=None) < datetime.now() - timedelta(minutes=10):
                raise CustomException(code=12, message=self.error_messages['token_expired'])

            return attrs
        except User.DoesNotExist:
            pass
        raise CustomException(code=10, message=self.error_messages['invalid_token'])


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_token': _('Token is invalid.'),
        'inactive_account': _('User account is disabled.'),
        'invalid_password': _('Password must have at least 6 characters.'),
    }

    def validate(self, attrs):
        token = attrs.get("token")
        password = attrs.get("password")
        if not token or not token.isdigit():
            raise CustomException(code=10, message=self.error_messages['invalid_token'])
        if not password or len(password) < 6:
            raise CustomException(code=11, message=self.error_messages['invalid_password'])

        try:
            user = User.objects.get(password_reset_token=int(token))
            if user.password_reset_sent_at:
                raise CustomException(code=10, message=self.error_messages['invalid_token'])
            if not user.is_active:
                raise CustomException(code=12, message=self.error_messages['inactive_account'])

            attrs['password'] = make_password(attrs['password'])
            return attrs
        except User.DoesNotExist:
            pass
        raise CustomException(code=10, message=self.error_messages['invalid_token'])


class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    current_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_current_password': _('Current_password is incorrect.'),
        'invalid_password': _('Password must have at least 6 characters.'),
        'invalid_user': _('User is invalid'),
    }

    def validate(self, attrs):
        current_password = attrs.get("current_password")
        new_password = attrs.get("new_password")
        user_id = attrs.get("user_id")
        print(user_id)

        if not current_password:
            raise CustomException(code=10, message=self.error_messages['invalid_current_password'])
        if not new_password or len(new_password) < 6:
            raise CustomException(code=11, message=self.error_messages['invalid_password'])

        user = User.objects.get(pk=user_id)
        if user.check_password(current_password):
            attrs['new_password'] = make_password(attrs['new_password'])
            return attrs
        else:
            raise CustomException(code=10, message=self.error_messages['invalid_current_password'])
