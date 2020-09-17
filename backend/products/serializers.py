from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from common.exception import CustomException
from products.models import Product, Category, Favorites, Purchases, Review
from users.models import User


class PostProductSerializer(serializers.ModelSerializer):
    assets = serializers.ListField(required=False)
    time = serializers.IntegerField(required=False)
    category_id = serializers.IntegerField(required=False)
    price = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    length = serializers.CharField(required=False)
    width = serializers.CharField(required=False)
    height = serializers.CharField(required=False)
    weight = serializers.CharField(required=False)
    tag = serializers.ListField(required=False)

    default_error_messages = {
        'invalid_assets': _('assets is invalid.'),
        'invalid_category': _('Category is not selected.'),
        'invalid_price': _('Price is invalid.'),
        'invalid_currency': _('Currency is selected.'),
        'invalid_title': _('Title is invalid.'),
        'invalid_description': _('Description was not selected.'),
        'invalid_length': _('Length was not selected.'),
        'invalid_width': _('Width was not selected.'),
        'invalid_height': _('Height was not selected.'),
        'invalid_weight': _('Weight was not selected.'),
    }

    class Meta:
        model = Product
        fields = ("assets", "time", "category_id", "price", "currency", "title", "description", "tag", "length",
                  "width", "height", "weight")

    def validate(self, attrs):
        assets = attrs.get("assets")
        category_id = attrs.get("category_id")
        price = attrs.get("price")
        currency = attrs.get("currency")
        title = attrs.get("title")
        description = attrs.get("description")
        length = attrs.get("length")
        width = attrs.get("width")
        height = attrs.get("height")
        weight = attrs.get("weight")

        if not assets:
            raise CustomException(code=15, message=self.error_messages['invalid_assets'])
        if not category_id:
            raise CustomException(code=10, message=self.error_messages['invalid_category'])
        if not (price and price.replace('.', '', 1).isdigit()):
            raise CustomException(code=11, message=self.error_messages['invalid_price'])
        if not currency:
            raise CustomException(code=12, message=self.error_messages['invalid_currency'])
        if not title:
            raise CustomException(code=13, message=self.error_messages['invalid_title'])
        if not description:
            raise CustomException(code=14, message=self.error_messages['invalid_description'])
        if not length:
            raise CustomException(code=16, message=self.error_messages['invalid_length'])
        if not width:
            raise CustomException(code=17, message=self.error_messages['invalid_width'])
        if not height:
            raise CustomException(code=18, message=self.error_messages['invalid_height'])
        if not weight:
            raise CustomException(code=19, message=self.error_messages['invalid_weight'])

        try:
            category = Category.objects.get(id=category_id)
            attrs['category'] = category
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=10, message=self.error_messages['invalid_category'])


class ProductUpdateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False)
    assets = serializers.ListField(required=False)
    category_id = serializers.IntegerField(required=False)
    price = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    tag = serializers.ListField(required=False)
    length = serializers.CharField(required=False)
    width = serializers.CharField(required=False)
    height = serializers.CharField(required=False)
    weight = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_product': _('product is invalid.'),
        'invalid_assets': _('assets is invalid.'),
        'invalid_category': _('Category is not selected.'),
        'invalid_price': _('Price is invalid.'),
        'invalid_currency': _('Currency is selected.'),
        'invalid_title': _('Title is invalid.'),
        'invalid_description': _('Description was not selected.'),
        'invalid_category_product': _('Category is not selected or product is invalid.'),
        'invalid_length': _('Length was not selected.'),
        'invalid_width': _('Width was not selected.'),
        'invalid_height': _('Height was not selected.'),
        'invalid_weight': _('Weight was not selected.'),
    }

    class Meta:
        model = Product
        fields = ("product_id", "assets", "time", "category_id", "price", "currency", "title", "description", "tag", "length",
                  "width", "height", "weight")

    def validate(self, attrs):
        product_id = attrs.get("product_id")
        assets = attrs.get("assets")
        category_id = attrs.get("category_id")
        price = attrs.get("price")
        currency = attrs.get("currency")
        title = attrs.get("title")
        description = attrs.get("description")
        length = attrs.get("length")
        width = attrs.get("width")
        height = attrs.get("height")
        weight = attrs.get("weight")

        if not product_id:
            raise CustomException(code=16, message=self.error_messages['invalid_product'])
        if not assets:
            raise CustomException(code=10, message=self.error_messages['invalid_assets'])
        if not category_id:
            raise CustomException(code=11, message=self.error_messages['invalid_category'])
        if not (price and price.replace('.', '', 1).isdigit()):
            raise CustomException(code=12, message=self.error_messages['invalid_price'])
        if not currency:
            raise CustomException(code=13, message=self.error_messages['invalid_currency'])
        if not title:
            raise CustomException(code=14, message=self.error_messages['invalid_title'])
        if not description:
            raise CustomException(code=15, message=self.error_messages['invalid_description'])
        if not length:
            raise CustomException(code=17, message=self.error_messages['invalid_length'])
        if not width:
            raise CustomException(code=18, message=self.error_messages['invalid_width'])
        if not height:
            raise CustomException(code=19, message=self.error_messages['invalid_height'])
        if not weight:
            raise CustomException(code=13, message=self.error_messages['invalid_weight'])

        try:
            category = Category.objects.get(id=category_id)
            product = Product.objects.get(id=product_id)
            attrs['category'] = category
            attrs['product'] = product
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=17, message=self.error_messages['invalid_category_product'])


class FavoriteSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_product': _('Product_id is invalid.'),
    }

    class Meta:
        model = Favorites
        fields = ("user_id", "product_id")

    def validate(self, attrs):
        product_id = attrs.get("product_id")

        if not product_id:
            raise CustomException(code=10, message=self.error_messages['invalid_product'])

        try:
            attrs['product'] = Product.objects.get(id=product_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=10, message=self.error_messages['invalid_product'])


class AddToCartViewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_product': _('Product_id is invalid.'),
    }

    class Meta:
        model = Purchases
        fields = ("user_id", "product_id", "state")

    def validate(self, attrs):
        product_id = attrs.get("product_id")

        if not product_id:
            raise CustomException(code=10, message=self.error_messages['invalid_product'])

        try:
            attrs['product'] = Product.objects.get(id=product_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=10, message=self.error_messages['invalid_product'])


class ReportProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_product': _('Product_id is invalid.'),
    }

    class Meta:
        model = Purchases
        fields = ("user_id", "product_id", "state")

    def validate(self, attrs):
        product_id = attrs.get("product_id")

        if not product_id:
            raise CustomException(code=10, message=self.error_messages['invalid_product'])

        try:
            attrs['report'] = Product.objects.get(id=product_id)
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=10, message=self.error_messages['invalid_product'])


class SendReviewSerializer(serializers.ModelSerializer):
    purchase_id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=False)
    msg = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_purchase': _('purchase_id is invalid'),
        'invalid_product': _('Product_id is invalid'),
        'Empty_msg': _('Review is Empty.'),
        'invalid_reviewable': _('Review is impossible.'),
    }

    class Meta:
        model = Review
        fields = ("purchase_id", "product_id", "msg")

    def validate(self, attrs):
        purchase_id = attrs.get("purchase_id")
        product_id = attrs.get("product_id")
        msg = attrs.get("msg")

        if not purchase_id:
            raise CustomException(code=10, message=self.error_messages['invalid_purchase'])
        if not product_id:
            raise CustomException(code=10, message=self.error_messages['invalid_product'])
        if not msg:
            raise CustomException(code=11, message=self.error_messages['Empty_msg'])

        try:
            attrs['product'] = Product.objects.get(id=product_id)
            attrs['reviewable'] = Purchases.objects.get(id=purchase_id, product=product_id, state='1')
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=12, message=self.error_messages['invalid_reviewable'])


class ItemRequestSerializer(serializers.ModelSerializer):
    assets = serializers.ListField(required=False)
    time = serializers.IntegerField(required=False)
    seller_id = serializers.IntegerField(required=False)
    price = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_assets': _('assets is invalid.'),
        'invalid_user': _('Seller is invalid.'),
        'invalid_price': _('Price is invalid.'),
        'invalid_currency': _('Currency is selected.'),
        'invalid_title': _('Title is invalid.'),
        'invalid_description': _('Description was not selected.'),
    }

    class Meta:
        model = Product
        fields = ("assets", "time", "seller_id", "price", "currency", "title", "description")

    def validate(self, attrs):
        assets = attrs.get("assets")
        seller_id = attrs.get("seller_id")
        price = attrs.get("price")
        currency = attrs.get("currency")
        title = attrs.get("title")
        description = attrs.get("description")

        if not assets:
            raise CustomException(code=15, message=self.error_messages['invalid_assets'])
        if not seller_id:
            raise CustomException(code=10, message=self.error_messages['invalid_user'])
        if not (price and price.replace('.', '', 1).isdigit()):
            raise CustomException(code=11, message=self.error_messages['invalid_price'])
        if not currency:
            raise CustomException(code=12, message=self.error_messages['invalid_currency'])
        if not title:
            raise CustomException(code=13, message=self.error_messages['invalid_title'])
        if not description:
            raise CustomException(code=14, message=self.error_messages['invalid_description'])

        try:
            seller = User.objects.get(id=seller_id)
            attrs['seller'] = seller
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=10, message=self.error_messages['invalid_user'])


# class SendFeedbackSerializer(serializers.ModelSerializer):
#     product_id = serializers.IntegerField(required=False)
#     rate = serializers.IntegerField(required=False)
#
#     default_error_messages = {
#         'invalid_product': _('Product_id is invalid'),
#         'Empty_rate': _('Rate is Empty.'),
#         'invalid_Feedback': _('Feedback is impossible.'),
#     }
#
#     class Meta:
#         model = Feedback
#         fields = ("product_id", "rate")
#
#     def validate(self, attrs):
#         product_id = attrs.get("product_id")
#         rate = attrs.get("rate")
#
#         if not product_id:
#             raise CustomException(code=10, message=self.error_messages['invalid_product'])
#         if not rate:
#             raise CustomException(code=11, message=self.error_messages['Empty_rate'])
#
#         try:
#             attrs['product'] = Product.objects.get(id=product_id)
#             attrs['Feedback'] = Purchases.objects.get(product=product_id, state='5')
#             return attrs
#         except ObjectDoesNotExist:
#             raise CustomException(code=12, message=self.error_messages['invalid_Feedback'])
