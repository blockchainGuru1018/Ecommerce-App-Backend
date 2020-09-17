from django.db import models
from users.models import User
from common.models import BaseModel


class Category(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    currency = models.CharField(blank=False, max_length=5, default='$')
    title = models.CharField(blank=False, max_length=255)
    description = models.TextField(null=True)
    request = models.IntegerField(blank=False, default='0')
    accept = models.IntegerField(blank=False, default='0')
    length = models.CharField(null=False, max_length=10, default='0')
    width = models.CharField(null=False, max_length=10, default='0')
    height = models.CharField(null=False, max_length=10, default='0')
    weight = models.CharField(null=False, max_length=10, default='0')
    available = models.BooleanField(blank=False, default='t')
    time = models.IntegerField(null=True)
    views = models.IntegerField(null=True, default='0')

    def __str__(self):
        return self.pk


class Asset(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.TextField(blank=False, max_length=255)

    def __str__(self):
        return self.pk


class Favorites(models.Model):
    class Meta:
        db_table = 'favorites'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.pk


class Purchases(BaseModel):
    class Meta:
        db_table = 'purchases'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    state = models.IntegerField(blank=False, default='0')
    paid = models.FloatField(null=True)
    payment_intent = models.TextField(null=True)
    label_url = models.CharField(null=True, max_length=255)
    tracking_number = models.TextField(null=True, max_length=255)
    object_id = models.CharField(null=True, max_length=255)
    transaction_state = models.BooleanField(blank=False, default='f')
    carrier_account = models.CharField(null=True, max_length=255)
    days = models.IntegerField(null=True, default='0')
    transaction_start = models.DateTimeField(null=True)
    transaction_end = models.DateTimeField(null=True)

    def __str__(self):
        return self.pk


class Review(BaseModel):
    class Meta:
        db_table = 'review'

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    msg = models.TextField(blank=False, max_length=255)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')

    def __str__(self):
        return self.pk


class Feedback(BaseModel):
    class Meta:
        db_table = 'feedback'

    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='giver')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(blank=False, default='0')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    def __str__(self):
        return self.pk


class Report(BaseModel):
    class Meta:
        db_table = 'report'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')

    def __str__(self):
        return self.pk


class HashTags(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.pk


class Request(BaseModel):
    class Meta:
        db_table = 'request'

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='request_product')
    accept = models.IntegerField(blank=False, default='0')

    def __str__(self):
        return self.pk
