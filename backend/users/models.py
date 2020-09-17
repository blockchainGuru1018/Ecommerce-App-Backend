from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import BaseModel


class User(AbstractUser):
    email = models.CharField(blank=False, max_length=255, unique=True)
    username = models.CharField(null=True, max_length=40, unique=True)
    password = models.CharField(null=True, max_length=128)
    first_name = None
    last_name = None
    name = models.CharField(blank=False, max_length=255)
    overview = models.TextField(null=True)
    avatar = models.CharField(null=True, max_length=255)
    address_name = models.CharField(null=True, max_length=255)
    address = models.CharField(null=True, max_length=255)
    city = models.CharField(null=True, max_length=255)
    state = models.CharField(null=True, max_length=255)
    Zip = models.CharField(null=True, max_length=255)
    phone = models.CharField(null=True, max_length=255)
    password_reset_token = models.IntegerField(null=True)
    password_reset_sent_at = models.DateTimeField(null=True)
    customer_id = models.CharField(null=True, max_length=255)
    client_id = models.CharField(null=True, max_length=255)
    push_notification_enabled = models.BooleanField(blank=False, default=True)
    sms_notification_enabled = models.BooleanField(blank=False, default=True)
    email_notification_enabled = models.BooleanField(blank=False, default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Following(models.Model):
    class Meta:
        db_table = 'following'

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')

    def __str__(self):
        return self.pk


class Payment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_name = models.CharField(blank=False, max_length=255)
    card_type = models.CharField(blank=False, max_length=255)
    card_number = models.CharField(blank=False, max_length=255)
    expiry = models.CharField(blank=False, max_length=255)
    cvv = models.CharField(blank=False, max_length=255)
    method_id = models.CharField(null=True, max_length=255)
