from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from common.exception import CustomException
import re

from users.models import User, Payment


class ShippingSerializer(serializers.ModelSerializer):
    address_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    Zip = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_address_name': _('Address_name field is empty.'),
        'invalid_address': _('Address field is empty.'),
        'invalid_city': _('City field is empty.'),
        'invalid_state': _('State field is empty.'),
        'invalid_Zip': _('Zip field is empty.'),
    }

    class Meta:
        model = User
        fields = ("address_name", "address", "city", "state", "Zip")

    def validate(self, attrs):
        address_name = attrs.get("address_name")
        address = attrs.get("address")
        city = attrs.get("city")
        state = attrs.get("state")
        Zip = attrs.get("Zip")

        if not address_name:
            raise CustomException(code=10, message=self.error_messages['invalid_address_name'])
        if not address:
            raise CustomException(code=10, message=self.error_messages['invalid_address'])
        if not city:
            raise CustomException(code=11, message=self.error_messages['invalid_city'])
        if not state:
            raise CustomException(code=12, message=self.error_messages['invalid_state'])
        if not Zip:
            raise CustomException(code=13, message=self.error_messages['invalid_Zip'])
        return attrs


class FollowingSerializer(serializers.Serializer):
    followed_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_followed': _('followed id failed.'),
    }

    def validate(self, attrs):
        followed_id = attrs.get("followed_id")

        if not followed_id:
            raise CustomException(code=10, message=self.error_messages['invalid_followed'])

        try:
            attrs['user_followed'] = User.objects.get(id=followed_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=10, message=self.error_messages['invalid_followed'])


class GetUserByIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_user': _('user id is invalid.'),
    }

    def validate(self, attrs):
        user_id = attrs.get("user_id")

        if not user_id:
            raise CustomException(code=10, message=self.error_messages['invalid_user'])

        try:
            attrs['user'] = User.objects.get(id=user_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=10, message=self.error_messages['invalid_user'])


class UpdateUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    avatar = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    overview = serializers.CharField(required=False)
    push_notification_enabled = serializers.BooleanField(required=False)
    sms_notification_enabled = serializers.BooleanField(required=False)
    email_notification_enabled = serializers.BooleanField(required=False)

    default_error_messages = {
        'invalid_username': _(
            'Username may only contain alphanumeric characters, and must be no more than 40 characters.'),
        'invalid_name': _('Your full name is required.'),
    }

    class Meta:
        model = User
        fields = ("user_id", "avatar", "username", "name", "overview", "push_notification_enabled",
                  "sms_notification_enabled", "email_notification_enabled")

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        username = attrs.get("username")
        name = attrs.get("name")

        if username:
            if not bool(re.match('^[a-zA-Z0-9]+$', username)) or len(username) > 40:
                raise CustomException(code=10, message=self.error_messages['invalid_username'])
            elif User.objects.filter(username=username).exclude(id=user_id).exists():
                raise CustomException(code=12, message=self.error_messages['duplicate_username'])
        if not name:
            raise CustomException(code=11, message=self.error_messages['invalid_name'])

        return attrs


class UserPaymentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    type = serializers.FileField(required=True)
    thru = serializers.CharField(required=True)
    cvv = serializers.CharField(required=True)

    default_error_messages = {
        'invalid_username': _(
            'Username may only contain alphanumeric characters, and must be no more than 40 characters.'),
        'invalid_name': _('Your full name is required.'),
    }

    class Meta:
        model = Payment
        fields = ("user_id", "type", "thru", "cvv")

    def validate(self, attrs):
        type = attrs.get("type")
        thru = attrs.get("thru")
        cvv = attrs.get("cvv")

        return attrs
