from django.core.mail import send_mail
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_auth.views import LoginView, LogoutView
from fcm_django.models import FCMDevice
from datetime import datetime
import random
import stripe

from common.serializers import serialize_featuring
from .serializers import RegistrationSerializer, ForgotSerializer, SocialLoginSerializer, ConfirmTokenSerializer, \
    ResetPasswordSerializer, ChangePasswordSerializer
from users.models import User
from products.models import Product, Favorites, Asset, Request, Category


class UserLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()
        device = FCMDevice()
        device.user = self.request.user
        device.registration_id = self.request.data.get('registration_id')
        device.save()

        response = {
            "result": True,
            "data": {
                "token": original_response.data.get('key'),
                "user": {
                    "id": self.user.id,
                    "email": self.user.email,
                    "username": self.user.username,
                    "name": self.user.name,
                    "avatar": self.user.avatar,
                    "address": self.user.address,
                    "phone": self.user.phone
                }
            }
        }

        return Response(response, status=status.HTTP_201_CREATED)


class UserRegistrationView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response({"result": True}, status=status.HTTP_201_CREATED, headers=headers)


class SocialLoginView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SocialLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device = FCMDevice()
        user_info = serializer.validated_data['user_info']
        provider = serializer.data.get('provider')

        try:
            user = User.objects.get(email=user_info['email'])
            device.user = user
            device.registration_id = request.data.get('registration_id')
            device.save()
        except ObjectDoesNotExist:
            user = User()
            if provider == 'google':
                user.email = user_info['email']
                user.name = user_info['name']
                user.avatar = user_info['picture']
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.name,
                )
                user.customer_id = customer.id
            user.save()
            device.user = user
            device.registration_id = request.data.get('registration_id')
            device.save()

        if not user.is_active:
            return Response(
                {
                    "result": False,
                    "errorCode": 13,
                    "errorMsg": "User account is disabled."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            token = Token.objects.get(user=user)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=user)
        response = {
            "result": True,
            "data": {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "name": user.name,
                    "avatar": user.avatar,
                    "address": user.address,
                    "phone": user.phone
                }
            }
        }

        return Response(response, status=status.HTTP_201_CREATED)


class ForgotPasswordView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ForgotSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data.get('username')
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)
            if user.is_active:
                token = random.randint(100000, 999999)
                user.password_reset_token = token
                user.password_reset_sent_at = datetime.now()
                user.save()
                send_mail(
                    'Subject here',
                    str(token),
                    'no-reply@unboxxen.com',
                    [user.email]
                )
        except ObjectDoesNotExist:
            pass

        headers = self.get_success_headers(serializer.data)
        return Response({"result": True}, status=status.HTTP_201_CREATED, headers=headers)


class ConfirmTokenView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ConfirmTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(password_reset_token=int(serializer.data.get('token')))
        user.password_reset_sent_at = None
        user.save()

        return Response({"result": True}, status=status.HTTP_201_CREATED)


class ResetPasswordView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(password_reset_token=int(serializer.data.get('token')))
        user.password = serializer.data.get('password')
        user.password_reset_token = None
        user.save()

        return Response({"result": True}, status=status.HTTP_201_CREATED)


class ChangePasswordView(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            'user_id': request.user.id,
            'current_password': request.data.get('current_password'),
            'new_password': request.data.get('new_password')
        })
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.password = serializer.data.get('new_password')
        user.save()

        return Response({"result": True}, status=status.HTTP_200_OK)


class UserLogoutView(LogoutView):
    def logout(self, request):
        FCMDevice.objects.filter(user=request.user).delete()
        super().logout(request)
        return Response({"result": True}, status=status.HTTP_201_CREATED)


class CategoryProductsView(GenericAPIView):

    def get(self, request):
        if request.user:
            user = request.user
        products_id = Request.objects.filter(accept=0).values_list('product_id', flat=True)
        category_list = Category.objects.all()
        cat_products = []

        for category in category_list:
            name = category.name
            hope = []
            products = Product.objects.filter(category=category).exclude(id__in=products_id).order_by('-views')
            for cat in products:
                assets = Asset.objects.filter(product_id=cat.id)
                if user:
                    is_favorite = Favorites.objects.filter(user=user.id, product=cat.id).exists()
                else:
                    is_favorite = False
                hope.append({
                    "assets": assets.values('url').order_by('created_at'),
                    **serialize_featuring(cat, is_favorite)
                })
            cat_products.append({
                hope
            })
        return Response(
            {
                "result": True,
                "data": {
                    "category-products": cat_products,
                }
            },
            status=status.HTTP_201_CREATED
        )


class NewestProductsView(GenericAPIView):

    def get(self, request):
        products_id = Request.objects.filter(accept=0).values_list('product_id', flat=True)
        newest = Product.objects.all().exclude(id__in=products_id).order_by('-created_at')

        new_products = []
        for new in newest:
            assets = Asset.objects.filter(product_id=new.id)
            new_products.append({
                "product_id": new.id,
                "title": new.title,
                "price": new.price,
                "currency": new.currency,
                "time": new.time,
                "assets": assets.values('url').order_by('created_at'),
            })
        return Response(
            {
                "result": True,
                "data": {
                    "newest-products": new_products,
                }
            },
            status=status.HTTP_201_CREATED
        )


class PopularProductsView(GenericAPIView):

    def get(self, request):
        products_id = Request.objects.filter(accept=0).values_list('product_id', flat=True)
        popular = Product.objects.all().exclude(id__in=products_id).annotate(num_favorites=Count('favorites')).order_by('-num_favorites')

        pop_products = []
        for pop in popular:
            assets = Asset.objects.filter(product_id=pop.id)
            pop_products.append({
                "product_id": pop.id,
                "title": pop.title,
                "price": pop.price,
                "currency": pop.currency,
                "time": pop.time,
                "assets": assets.values('url').order_by('created_at'),
            })
        return Response(
            {
                "result": True,
                "data": {
                    "popular-products": pop_products,
                }
            },
            status=status.HTTP_201_CREATED
        )
