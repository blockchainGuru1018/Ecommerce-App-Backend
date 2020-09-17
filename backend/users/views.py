from django.db.models import Avg
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from datetime import datetime
import stripe

from users.models import Following
from users.serializers import ShippingSerializer, FollowingSerializer, GetUserByIdSerializer, UpdateUserSerializer
from products.models import Favorites, Purchases, Asset, Product, Feedback, Review, Request
from users.models import User, Payment
from common.serializers import Following_Notification, Following_mail


class UserDetailView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = GetUserByIdSerializer

    def get(self, request, pk):
        serializer = self.get_serializer(data={"user_id": pk})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        products_id = Request.objects.filter(accept=0).values_list('product_id', flat=True)
        if user == request.user:
            favorites = Favorites.objects.filter(user=user)
            purchases = Purchases.objects.filter(user=user).exclude(state='0')
            mine = Product.objects.filter(user=pk).exclude(id__in=products_id)

            fav_products = []
            for fav in favorites:
                assets = Asset.objects.filter(product_id=fav.id)
                is_favorite = Favorites.objects.filter(user=user, product=fav.product.id).exists()
                fav_products.append({
                    "product_id": fav.product.id,
                    "title": fav.product.title,
                    "price": fav.product.price,
                    "currency": fav.product.currency,
                    "time": fav.product.time,
                    "favorite": is_favorite,
                    "assets": assets.values('url')[:1],
                })

            pur_products = []
            for pur in purchases:
                assets = Asset.objects.filter(product=pur.product)
                is_favorite = Favorites.objects.filter(user=user, product=pur.product.id).exists()
                pur_products.append({
                    "product_id": pur.product.id,
                    "title": pur.product.title,
                    "price": pur.product.price,
                    "currency": pur.product.currency,
                    "time": pur.product.time,
                    "favorite": is_favorite,
                    "assets": assets.values('url')[:1],
                })

            my_products = []
            for my in mine:
                assets = Asset.objects.filter(product_id=my.id)
                my_products.append({
                    "product_id": my.id,
                    "title": my.title,
                    "price": my.price,
                    "currency": my.currency,
                    "time": my.time,
                    "assets": assets.values('url')[:1],
                })

            return Response(
                {
                    "result": True,
                    "data": {
                        "avatar": user.avatar,
                        "name": user.name,
                        "my_products": my_products,
                        "purchases": pur_products,
                        "favorites": fav_products,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        else:
            current_month = datetime.now().month
            currents = Product.objects.filter(user=user, available=True).exclude(id__in=products_id)
            monthly = Product.objects.filter(user=user, created_at__month=current_month).exclude(id__in=products_id)
            avg_feedback = Feedback.objects.filter(receiver=user).aggregate(Avg('rate'))
            num_reviews = Review.objects.filter(seller=user).count()
            followed = False
            if Following.objects.filter(followed=pk, follower=request.user).exists():
                followed = True

            cur_products = []
            for cur in currents:
                assets = Asset.objects.filter(product_id=cur.id)
                is_favorite = Favorites.objects.filter(user=user, product=cur).exists()
                cur_products.append({
                    "product_id": cur.id,
                    "title": cur.title,
                    "price": cur.price,
                    "currency": cur.currency,
                    "time": cur.time,
                    "favorite": is_favorite,
                    "assets": assets.values('url')[:1],
                })

            mon_products = []
            for mon in monthly:
                assets = Asset.objects.filter(product_id=mon.id)
                is_favorite = Favorites.objects.filter(user=user, product=mon).exists()
                mon_products.append({
                    "product_id": mon.id,
                    "title": mon.title,
                    "price": mon.price,
                    "currency": mon.currency,
                    "time": mon.time,
                    "favorite": is_favorite,
                    "assets": assets.values('url')[:1],
                })

            return Response(
                {
                    "result": True,
                    "data": {
                        "avatar": user.avatar,
                        "name": user.name,
                        "username": user.username,
                        "followed": followed,
                        "feedback": avg_feedback,
                        "number of reviews": num_reviews,
                        "overview": user.overview,
                        "currents": cur_products,
                        "monthly": mon_products,
                    }
                },
                status=status.HTTP_201_CREATED
            )


class UserSettingView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        client_id = "ca_H9NLRtgnmxUhlJQd100UkRVTqHSbyNFl"
        user = request.user
        try:
            me = User.objects.get(id=user.id)
            my_payments = Payment.objects.filter(user=me)

            payments_array = []
            for payment in my_payments:
                payments_array.append({
                    "id": payment.id,
                    "card_name": payment.card_name,
                    "card_number": payment.card_number
                })

            info_list = []
            if me.client_id:
                r = stripe.Account.list_external_accounts(
                  me.client_id,
                  object="bank_account"
                )
                # r = stripe.Account.retrieve(me.client_id)
                infos = r.data
                for info in infos:
                    info_list.append({
                        "id": info.id,
                        "name": info.bank_name,
                        "number": info.last4,
                        "favorite": info.default_for_currency
                    })

            return Response(
                {
                    "result": True,
                    "data": {
                        "avatar": me.avatar,
                        "name": me.name,
                        "overview": me.overview,
                        "address_name": me.address,
                        "address": me.address,
                        "city": me.city,
                        "state": me.state,
                        "Zip": me.Zip,
                        "cards": payments_array,
                        "banks": info_list,
                        "add_bank_link": "https://connect.stripe.com/express/oauth/authorize?redirect_uri=https://connect.stripe.com/connect/default/oauth/test&client_id=" + client_id + "&state={STATE_VALUE}",
                        "push_notification_enabled": me.push_notification_enabled,
                        "email_notification_enabled": me.email_notification_enabled,
                        "sms_notification_enabled": me.sms_notification_enabled,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "User not found."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserSettingUpdate(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = UpdateUserSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.avatar = serializer.data.get('avatar')
        request.user.username = serializer.data.get('username')
        request.user.name = serializer.data.get('name')
        request.user.overview = serializer.data.get('overview')
        request.user.push_notification_enabled = serializer.data.get('push_notification_enabled')
        request.user.email_notification_enabled = serializer.data.get('email_notification_enabled')
        request.user.sms_notification_enabled = serializer.data.get('sms_notification_enabled')
        request.user.save()

        return Response({"result": True}, status=status.HTTP_201_CREATED)


class UsersShippingView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = ShippingSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.address_name = serializer.data.get('address_name')
        user.address = serializer.data.get('address')
        user.city = serializer.data.get('city')
        user.state = serializer.data.get('state')
        user.Zip = serializer.data.get('Zip')
        user.save()
        return Response({"result": True}, status=status.HTTP_201_CREATED)


class FollowView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = FollowingSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_followed = serializer.validated_data['user_followed']
        is_followed = Following.objects.filter(follower=request.user, followed=user_followed).exists()

        if is_followed:
            Following.objects.filter(follower=request.user, followed=user_followed).delete()
            Following_Notification(user_followed, request.user, 0)
            Following_mail(user_followed, request.user, 0)
            return Response({"result": True}, status=status.HTTP_201_CREATED)
        else:
            follow = Following(follower=request.user, followed=user_followed)
            follow.save()
            Following_Notification(user_followed, request.user, 1)
            Following_mail(user_followed, request.user, 1)
            return Response({"result": True}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        users_followed = Following.objects.filter(follower=user)

        follows = []
        for fol in users_followed:
            follows.append({
                "id": fol.followed.id,
                "avatar": fol.followed.avatar,
                "fullname": fol.followed.name,
            })
        return Response(
            {
                "result": True,
                "data": {
                    "users": follows,
                }
            },
            status=status.HTTP_201_CREATED
        )


class UserPaymentView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        payment = Payment()
        payment.user = request.user
        payment.card_name = request.POST.get('card_name')
        payment.card_number = request.POST.get('card_number')
        payment.expiry = request.POST.get('expiry')
        payment.cvv = request.POST.get('cvv')
        exp = payment.expiry.split('.')
        try:
            p_method = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": payment.card_number,
                    "exp_month": exp[1],
                    "exp_year": exp[0],
                    "cvc": payment.cvv,
                },
            )
            stripe.PaymentMethod.attach(
                p_method,
                customer=request.user.customer_id,
            )
        except stripe.error.CardError:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Invalid Card info provided."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except stripe.error.RateLimitError:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Invalid Card RateLimit."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except stripe.error.InvalidRequestError:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Invalid Request provided."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except stripe.error.AuthenticationError:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Invalid Authentication."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except stripe.error.APIConnectionError:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Invalid APIConnection."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except stripe.error.StripeError:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Failed to add payment."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        payment.method_id = p_method.id
        payment.card_type = p_method.card.brand
        payment.save()

        return Response(
            {
                "result": True,
                "data": {
                    "msg": "Card created",
                    "card_id": payment.id,
                }
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        user = request.user
        try:
            me = User.objects.get(id=user.id)
            my_payments = Payment.objects.filter(user=me)

            payments_array = []
            for payment in my_payments:
                payments_array.append({
                    "id": payment.id,
                    "card_name": payment.card_name,
                    "card_type": payment.card_type,
                    "card_number": '****' + payment.card_number[-4:],
                    "expiry": payment.expiry,
                })
            return Response(
                {
                    "result": True,
                    "data": {
                        "cards": payments_array,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "User not found."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserCardDeleteView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    # def get(self, request, pk):
    #     user = request.user
    #     try:
    #         me = User.objects.get(id=user.id)
    #         payment = Payment.objects.get(user=me, id=pk)
    #         return Response(
    #             {
    #                 "result": True,
    #                 "data": {
    #                     "id": payment.id,
    #                     "customer_id": me.customer_id,
    #                     "method_id": payment.method_id,
    #                 }
    #             },
    #             status=status.HTTP_201_CREATED
    #         )
    #     except ObjectDoesNotExist:
    #         return Response(
    #             {
    #                 "result": False,
    #                 "errorCode": 3,
    #                 "errorMsg": "Card not found."
    #             },
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

    def delete(self, request, pk):
        try:
            payment = Payment.objects.get(user=request.user, id=pk)
            stripe.PaymentMethod.detach(payment.method_id)
            payment.delete()
            return Response({"result": True}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "Card not found."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BankdeleteView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def delete(self, request):
        stripe.Account.delete_external_account(
            request.user.client_id,
            request.GET.get('bank_id'),
        )
        return Response({"result": True}, status=status.HTTP_200_OK)


class BankFavoriteView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        stripe.Account.modify_external_account(
            request.user.client_id,
            request.POST.get('bank_id'),
            default_for_currency=True,
        )
        return Response({"result": True}, status=status.HTTP_200_OK)


class BankAddView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        response = stripe.OAuth.token(
            grant_type='authorization_code',
            code=request.POST.get('code'),
        )
        client_id = dict(response)
        print(client_id)

        request.user.client_id = client_id['stripe_user_id']
        request.user.save()
        return Response({"result": True}, status=status.HTTP_201_CREATED)


# class SellersView(GenericAPIView):
#     authentication_classes = (TokenAuthentication,)
#
#     def get(self, request):
#         sellers = Product.objects.values_list('user_id').distinct()
#         print(sellers)
#
#         ProductPost_Notification()
#
#         sellers_list = []
#         for seller in sellers:
#             user = User.objects.get(pk=seller)
#             sellers_list.append({
#                 "id": user.id,
#                 "fullname": user.name,
#             })
#         return Response(
#             {
#                 "result": True,
#                 "data": {
#                     "users": sellers_list,
#                 }
#             },
#             status=status.HTTP_201_CREATED
#         )

