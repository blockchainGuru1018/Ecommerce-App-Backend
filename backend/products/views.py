from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
import stripe
import shippo
from shippo import error
import requests
from datetime import datetime
import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import PostProductSerializer, ProductUpdateSerializer, FavoriteSerializer, AddToCartViewSerializer, \
    ReportProductSerializer, SendReviewSerializer, ItemRequestSerializer
from products.models import Product, Asset, Favorites, Purchases, Feedback, Review, Report, HashTags, Category, \
    Request
from users.models import Payment
from common.serializers import Favorite_Notification, ProductCheckout_Notification, Confirm_Notification, ProductArrive_Notification, \
    ItemRequest_Notification, Favorite_mail, ProductArrive_mail, Confirm_mail, ProductCheckout_mail, ItemRequest_mail, \
    Accept_Notification, Accept_mail


class ProductUploadView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = PostProductSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product()
        product.user = request.user
        product.category = serializer.validated_data['category']
        product.price = float(serializer.data.get('price'))
        product.currency = serializer.data.get('currency')
        product.title = serializer.data.get('title')
        product.description = serializer.data.get('description')
        product.time = serializer.data.get('time')
        product.length = serializer.data.get('length')
        product.width = serializer.data.get('width')
        product.height = serializer.data.get('height')
        product.weight = serializer.data.get('weight')
        product.save()

        assets = serializer.data.get('assets')
        if assets:
            for url in assets:
                asset = Asset(product=product, url=url)
                asset.save()

        tags = serializer.data.get('tag')
        if tags:
            for t in tags:
                tag = HashTags(product=product, tag=t)
                tag.save()
        # ProductPost_Notification(user)
        return Response(
            {
                "result": True,
                "data": {
                    "Msg": "product created",
                    "product_id": product.id,
                }

            },
            status=status.HTTP_201_CREATED
        )


class ProductUpdateView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = ProductUpdateSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        product.user = request.user
        product.category = serializer.validated_data['category']
        product.price = float(serializer.data.get('price'))
        product.currency = serializer.data.get('currency')
        product.title = serializer.data.get('title')
        product.description = serializer.data.get('description')
        product.length = serializer.data.get('length')
        product.width = serializer.data.get('width')
        product.height = serializer.data.get('height')
        product.weight = serializer.data.get('weight')
        product.save()

        assets = serializer.data.get('assets')
        if assets:
            for url in assets:
                asset = Asset(product=product, url=url)
                asset.save()

        tags = serializer.data.get('tag')
        if tags:
            for t in tags:
                tag = HashTags(product=product, tag=t)
                tag.save()
        return Response(
            {
                "result": True,
                "data": {
                    "Msg": "product updated",
                    "product_id": product.id,
                }
            },
            status=status.HTTP_201_CREATED
        )


class ProductDetailView(GenericAPIView):

    def get(self, request, pk):
        if request.user:
            user = request.user
        try:
            product = Product.objects.get(id=pk)
            assets = Asset.objects.filter(product_id=pk)
            if user:
                is_favorite = Favorites.objects.filter(user=user.id, product=product).exists()
            else:
                is_favorite = False
            product.views = product.views+1
            product.save()
            avg_feedback = Feedback.objects.filter(receiver=product.user).aggregate(Avg('rate'))
            num_reviews = Review.objects.filter(seller=product.user).count()

            return Response(
                {
                    "result": True,
                    "data": {
                        "title": product.title,
                        "description": product.description,
                        "price": product.price,
                        "currency": product.currency,
                        "length": product.length,
                        "width": product.width,
                        "height": product.height,
                        "weight": product.weight,
                        "time": product.time,
                        "favorite": is_favorite,
                        "category_id": product.category.id,
                        "assets": assets.values('url'),
                        "owner": {
                            "id": product.user.id,
                            "avatar": product.user.avatar,
                            "name": product.user.name,
                            "feedback": avg_feedback,
                            "number of reviews": num_reviews,
                        }
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "Product not found."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SearchDetailView(GenericAPIView):

    def get(self, request):
        if request.user:
            me = request.user
        keyword = request.GET.get('keyword')
        category = request.GET.get('category_id')
        page = request.GET.get('page')
        if category:
            products_id = Request.objects.filter(accept=0).values_list('product_id', flat=True)
            search_product = Product.objects.filter(title__icontains=keyword, category=category).exclude(id__in=products_id).order_by('-updated_at')
        else:
            products_id = Request.objects.filter(accept=0).values_list('product_id', flat=True)
            search_product = Product.objects.all().exclude(id__in=products_id).order_by('-updated_at')

        paginator = Paginator(search_product, 5)
        try:
            search = paginator.page(page)
        except PageNotAnInteger:
            search = paginator.page(1)
        except EmptyPage:
            search = []

        sea_products = []
        for sea in search:
            assets = Asset.objects.filter(product_id=sea)
            if me:
                is_favorite = Favorites.objects.filter(user=me.id, product=sea).exists()
            else:
                is_favorite = False
            sea_products.append({
                "product_id": sea.id,
                "title": sea.title,
                "price": sea.price,
                "currency": sea.currency,
                "favorite": is_favorite,
                "category": sea.category_id,
                "time": sea.time,
                "assets": assets.values('url')[:1],
            })
        return Response(
            {
                "result": True,
                "data": {
                    "products": sea_products,
                }
            },
            status=status.HTTP_201_CREATED
        )


class FavoriteProductView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = FavoriteSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        is_favorite = Favorites.objects.filter(user=request.user, product=product).exists()

        if is_favorite:
            Favorites.objects.filter(user=request.user, product=product).delete()
            Favorite_Notification(product.user, request.user, 0, product.id)
            Favorite_mail(product.user, request.user, 0)
            return Response({"result": True}, status=status.HTTP_201_CREATED)
        else:
            favorite = Favorites(user=request.user, product=product)
            favorite.save()
            Favorite_Notification(product.user, request.user, 1, product.id)
            Favorite_mail(product.user, request.user, 1)
            return Response({"result": True}, status=status.HTTP_201_CREATED)


class MyCartView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = AddToCartViewSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        is_cart = Purchases.objects.filter(user=request.user, product=product, state='0')
        if is_cart:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Product already added."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            purchase = Purchases(user=request.user, product=product)
            purchase.save()
            return Response({"result": True}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        is_cart = Purchases.objects.filter(user=request.user, product=product, state='0')
        if is_cart:
            Purchases.objects.filter(user=request.user, product=product).delete()
            return Response({"result": True}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Product is invalid."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        user = request.user
        purchases = Purchases.objects.filter(user=user, state='0')

        products = []
        for pur in purchases:
            assets = Asset.objects.filter(product_id=pur.product_id)
            products.append({
                "product_id": pur.product.id,
                "title": pur.product.title,
                "price": pur.product.price,
                "currency": pur.product.currency,
                "time": pur.product.time,
                "assets": assets.values('url')[:1],
            })
        return Response(
            {
                "result": True,
                "data": {
                    "products": products,
                }
            },
            status=status.HTTP_201_CREATED
        )


class ReportView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = ReportProductSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reported_id = serializer.validated_data['report']
        is_report = Report.objects.filter(reporter=request.user, product=reported_id)
        if is_report:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Product already reported."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            report = Report(reporter=request.user, product=reported_id, user=reported_id.user)
            report.save()
            return Response({"result": True}, status=status.HTTP_201_CREATED)


class ReviewableProductsView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = request.user
        purchases = Purchases.objects.filter(user=user, state='1')

        products = []
        for pur in purchases:
            assets = Asset.objects.filter(product_id=pur.product_id)
            products.append({
                "purchase_id": pur.id,
                "product_id": pur.product.id,
                "title": pur.product.title,
                "price": pur.product.price,
                "currency": pur.product.currency,
                "time": pur.product.time,
                "date of purchase": pur.updated_at,
                "assets": assets.values('url')[:1],
            })
        return Response(
            {
                "result": True,
                "data": {
                    "products": products,
                }
            },
            status=status.HTTP_201_CREATED
        )


class GetCategoryList(GenericAPIView):

    def get(self, request):
        categories = Category.objects.all().values('id', 'name')
        return Response(
            {
                "result": True,
                "data": categories
            },
            status=status.HTTP_201_CREATED
        )


class PurchaseMountView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        total = 0
        delivery = 0
        purchases = Purchases.objects.filter(user=request.user, state='0')
        if not purchases:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "Your Cart is Empty."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            for purchase in purchases:
                seller = purchase.product.user
                buyer = request.user
                price = purchase.product.price
                total = total + price
                product = purchase.product

                address_from = {
                    "name": seller.address_name,
                    "street1": seller.address,
                    "city": seller.city,
                    "state": seller.state,
                    "zip": seller.Zip,
                    "country": "US"
                }

                address_to = {
                    "name": buyer.address_name,
                    "street1": buyer.address,
                    "city": buyer.city,
                    "state": buyer.state,
                    "zip": buyer.Zip,
                    "country": "US"
                }

                parcel = {
                    "length": product.length,
                    "width": product.width,
                    "height": product.height,
                    "distance_unit": "in",
                    "weight": product.weight,
                    "mass_unit": "lb"
                }

                try:
                    shipment = shippo.Shipment.create(
                        address_from=address_from,
                        address_to=address_to,
                        parcels=[parcel],
                        async=False
                    )
                    fee = float(shipment.rates[0].amount)
                    print(fee)
                    delivery = delivery + fee
                except error.AddressError:
                    return Response(
                        {
                            "result": False,
                            "errorCode": 1,
                            "errorMsg": product.title + " can't be delivered."
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                except error.InvalidRequestError:
                    return Response(
                        {
                            "result": False,
                            "errorCode": 1,
                            "errorMsg": product.title + " can't be delivered."
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                except error.ShippoError:
                    return Response(
                        {
                            "result": False,
                            "errorCode": 1,
                            "errorMsg": product.title + " can't be delivered."
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        return Response(
            {
                "result": True,
                "data": {
                    "total_product_price": total,
                    "total_delivery_fee": delivery,
                    "total_price": total + delivery
                }

            },
            status=status.HTTP_201_CREATED
        )


class CheckoutProductsView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        purchases = Purchases.objects.filter(user=request.user, state='0')
        if not purchases:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "Your Cart is Empty."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            error_msg = []
            label_url = []
            for purchase in purchases:
                seller = purchase.product.user
                buyer = request.user
                product = purchase.product
                try:
                    card_id = Payment.objects.get(id=request.POST.get('card_id')).method_id

                    try:
                        payment_intent = stripe.PaymentIntent.create(
                            payment_method_types=['card'],
                            amount=int(purchase.product.price*100),
                            currency='usd',
                            application_fee_amount=int(purchase.product.price*10),
                            payment_method=card_id,
                            transfer_data={
                                'destination': seller.client_id,
                            },
                            customer=request.user.customer_id
                        )
                        purchase.payment_intent = payment_intent.id
                        purchase.save()

                        address_from = {
                            "name": seller.address_name,
                            "street1": seller.address,
                            "city": seller.city,
                            "state": seller.state,
                            "zip": seller.Zip,
                            "country": "US"
                        }

                        address_to = {
                            "name": buyer.address_name,
                            "street1": buyer.address,
                            "city": buyer.city,
                            "state": buyer.state,
                            "zip": buyer.Zip,
                            "country": "US"
                        }

                        parcel = {
                            "length": product.length,
                            "width": product.width,
                            "height": product.height,
                            "distance_unit": "in",
                            "weight": product.weight,
                            "mass_unit": "lb"
                        }

                        shipment = shippo.Shipment.create(
                            address_from=address_from,
                            address_to=address_to,
                            parcels=[parcel],
                            async=False
                        )
                        fee = float(shipment.rates[0].amount)

                        delivery_intent = stripe.PaymentIntent.create(
                            payment_method_types=['card'],
                            amount=int(fee*100),
                            currency='usd',
                            payment_method=card_id,
                            customer=request.user.customer_id
                        )
                        stripe.PaymentIntent.confirm(
                            delivery_intent.id,
                        )

                        rate = shipment.rates[0]
                        transaction = shippo.Transaction.create(
                            rate=rate.object_id,
                            label_file_type="PDF",
                            async=False
                        )
                        if transaction.status == "SUCCESS":
                            label_url.append({
                                "label_url": transaction.label_url
                            })
                            purchase.label_url = transaction.label_url
                            purchase.tracking_number = transaction.tracking_number
                            purchase.object_id = transaction.object_id
                            purchase.carrier_account = rate.carrier_account
                            purchase.days = rate.estimated_days
                            purchase.transaction_start = rate.object_created
                            purchase.state = '1'
                            purchase.save()
                            ProductCheckout_Notification(seller, buyer, product, purchase.label_url)
                            ProductCheckout_mail(seller, buyer, product.title, purchase.label_url)
                        else:
                            error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": transaction.messages,
                            })

                    except error.AddressError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "AddressError",
                        })
                    except error.InvalidRequestError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "InvalidRequestError",
                        })
                    except error.ShippoError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "ShippoError",
                        })
                    except stripe.error.CardError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "CardError",
                        })
                    except stripe.error.RateLimitError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "RateLimitError",
                        })
                    except stripe.error.InvalidRequestError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "InvalidRequestError",
                        })
                    except stripe.error.AuthenticationError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "AuthenticationError",
                        })
                    except stripe.error.APIConnectionError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "APIConnectionError",
                        })
                    except stripe.error.StripeError:
                        error_msg.append({
                                "product_name": product.title,
                                "purchase_id": purchase.id,
                                "error_msg": "StripeError",
                        })

                except ObjectDoesNotExist:
                    return Response(
                        {
                            "result": False,
                            "errorCode": 3,
                            "errorMsg": "Card not found."
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        if error_msg:
            return Response(
                {
                    "result": True,
                    "error_list": error_msg,
                    "label_url": label_url
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "result": True,
                    "label_url": label_url
                },
                status=status.HTTP_201_CREATED
            )


class SendReview(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = SendReviewSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        purchase_id = serializer.data.get('purchase_id')
        try:
            purchase = Purchases.objects.get(id=purchase_id, product=product, user=request.user, state='1')
            print(purchase.id)
            stripe.PaymentIntent.confirm(
                purchase.payment_intent,
            )
            purchase.state = '2'
            purchase.save()
            Confirm_Notification(product.user, request.user, purchase.product)
            Confirm_mail(product.user, request.user, purchase.product.title)
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "purchase not found."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        msg = serializer.data.get('msg')
        rate = int(request.POST.get('rate'))
        review = Review(msg=msg, buy=request.user, product=product, sell=product.user)
        review.save()
        sendreview = Feedback(rate=rate, giver=request.user, product=product, receiver=product.user)
        sendreview.save()

        return Response({"result": True}, status=status.HTTP_201_CREATED)


class UpdateProductListView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        products = Product.objects.filter(user=request.user, available=True).exclude(accept=0, request=1)

        update_products = []
        for product in products:
            assets = Asset.objects.filter(product_id=product.id).count()
            if assets < 5:
                assets = Asset.objects.filter(product_id=product.id)
                update_products.append({
                    "id": product.id,
                    "assets": assets.values('url')[:1],
                })

        return Response(
            {
                "result": True,
                "data": {
                    "update_products": update_products,
                }
            },
            status=status.HTTP_201_CREATED
        )


class RequestedProductListView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        products_id = Request.objects.filter(seller=request.user, accept=0).values_list('product_id', flat=True)
        products = Product.objects.filter(id__in=products_id)

        requested_products = []
        for product in products:
            assets = Asset.objects.filter(product_id=product.id)
            requested_products.append({
                "id": product.id,
                "buyer_name": product.user.name,
                "product_title": product.title,
                "product_price": product.price,
                "assets": assets.values('url')[:1],
            })

        return Response(
            {
                "result": True,
                "data": {
                    "requested_products": requested_products,
                }
            },
            status=status.HTTP_201_CREATED
        )


class OfferedProductListView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        products_id = Request.objects.filter(buyer=request.user, accept=1).values_list('product_id', flat=True)
        products = Product.objects.filter(id__in=products_id)

        offered_products = []
        for product in products:
            assets = Asset.objects.filter(product_id=product.id)
            offered_products.append({
                "id": product.id,
                "seller_name": product.user.name,
                "assets": assets.values('url')[:1],
            })

        return Response(
            {
                "result": True,
                "data": {
                    "offered_products": offered_products,
                }
            },
            status=status.HTTP_201_CREATED
        )


class FullProductView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = ProductUpdateSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        product.user = request.user
        product.category = serializer.validated_data['category']
        product.price = float(serializer.data.get('price'))
        product.currency = serializer.data.get('currency')
        product.title = serializer.data.get('title')
        product.description = serializer.data.get('description')
        product.length = serializer.data.get('length')
        product.width = serializer.data.get('width')
        product.height = serializer.data.get('height')
        product.weight = serializer.data.get('weight')
        product.accept = 1
        product.save()
        accept = Request.objects.get(product=product)
        accept.accept = 1
        accept.save()
        old_assets_id = Asset.objects.filter(product=product).delete()

        assets = serializer.data.get('assets')
        if assets:
            for url in assets:
                asset = Asset(product=product, url=url)
                asset.save()

        tags = serializer.data.get('tag')
        if tags:
            for t in tags:
                tag = HashTags(product=product, tag=t)
                tag.save()
        Accept_Notification(product.user, accept.buyer, product.id)
        Accept_mail(product.user, accept.buyer)
        return Response(
            {
                "result": True,
                "data": {
                    "Msg": "product accepted and uploaded",
                    "product_id": product.id,
                }
            },
            status=status.HTTP_201_CREATED
        )


class DeclineProductView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            return Response({"result": True}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "Product not found."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Tracking(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        try:
            purchase = Purchases.objects.get(id=pk)
            payload = {
                "carrier": purchase.carrier_account,
                "tracking_number": purchase.tracking_number,
            }
            r = requests.post(
                'https://api.goshippo.com/tracks/',
                payload,
                headers={'Authorization': 'ShippoToken ' + shippo.config.api_key},
            )
            data = r.json()
            return Response(
                {
                    "result": True,
                    "data": {
                        "status": data['tracking_status'],
                        "history": data['tracking_history']
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "Transaction not found."
                }
            )


class TrackingWebHook(GenericAPIView):

    def post(self, request):
        tracking_number = request.data.get('data')['tracking_number']
        try:
            purchase = Purchases.objects.get(tracking_number=tracking_number, transaction_state=False)
            purchase.transaction_state = True
            purchase.transaction_end = request.data.get('data')['object_updated']
            purchase.save()
            ProductArrive_Notification(request.user, purchase.product)
            ProductArrive_mail(request.user, purchase.product.title)

            return Response({"result": True}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "Transaction not found."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrdersView(GenericAPIView):

    def get(self, request):
        CurrentOrders = Purchases.objects.filter(user=request.user, transaction_state=False)
        CurrentOrders_count = Purchases.objects.filter(user=request.user, transaction_state=False).count()
        PreviousOrders = Purchases.objects.filter(user=request.user, transaction_state=True)
        PreviousOrders_count = Purchases.objects.filter(user=request.user, transaction_state=True).count()

        CurrentOrders_list = []
        for CurrentOrder in CurrentOrders:
            buyer = request.user
            seller = CurrentOrder.product.user
            CurrentOrders_list.append({
                "purchase_id": CurrentOrder.id,
                "Product_name": CurrentOrder.product.title,
                "address_from": seller.city,
                "transaction_start_at": CurrentOrder.transaction_start,
                "address_to": buyer.city,
                "transaction_end_at": CurrentOrder.transaction_start + datetime.timedelta(days=CurrentOrder.days),
            })

        PreviousOrders_list = []
        for PreviousOrder in PreviousOrders:
            buyer = request.user
            seller = PreviousOrder.product.user
            PreviousOrders_list.append({
                "purchase_id": PreviousOrder.id,
                "Product_name": PreviousOrder.product.title,
                "address_from": seller.city,
                "transaction_start_at": PreviousOrder.transaction_start,
                "address_to": buyer.city,
                "transaction_end_at": PreviousOrder.transaction_end,
            })

        return Response(
            {
                "result": True,
                "data": {
                    "CurrentOrders_count": CurrentOrders_count,
                    "CurrentOrders": CurrentOrders_list,
                    "PreviousOrders_count": PreviousOrders_count,
                    "PreviousOrders": PreviousOrders_list,
                }
            }
        )


class ItemRequest(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = ItemRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product()
        product.user = request.user
        product.price = float(serializer.data.get('price'))
        product.currency = serializer.data.get('currency')
        product.title = serializer.data.get('title')
        product.description = serializer.data.get('description')
        product.category = Category.objects.get(id=1)
        product.time = serializer.data.get('time')
        product.length = 0
        product.width = 0
        product.height = 0
        product.weight = 0
        product.request = 1
        product.accept = 0
        product.save()

        requested = Request()
        requested.seller = serializer.validated_data['seller']
        requested.buyer = request.user
        requested.product = product
        requested.save()

        assets = serializer.data.get('assets')
        if assets:
            for url in assets:
                asset = Asset(product=product, url=url)
                asset.save()
        ItemRequest_Notification(requested.seller, request.user, product)
        ItemRequest_mail(requested.seller, request.user, product)

        return Response(
            {
                "result": True,
                "data": {
                    "Msg": "Item Request created",
                    "Request_id": requested.id,
                }
            },
            status=status.HTTP_201_CREATED
        )
