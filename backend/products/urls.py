from django.urls import path
from .views import ProductUploadView, ProductUpdateView, ProductDetailView, SearchDetailView, FavoriteProductView, MyCartView, ReportView, \
    ReviewableProductsView, SendReview, GetCategoryList, CheckoutProductsView, UpdateProductListView, PurchaseMountView, Tracking, TrackingWebHook, \
    OrdersView, ItemRequest, RequestedProductListView, OfferedProductListView, FullProductView, DeclineProductView

app_name = 'products'

urlpatterns = [
    path('', ProductUploadView.as_view()),
    path('update/', ProductUpdateView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
    path('profile/update/', UpdateProductListView.as_view()),
    path('profile/requested/', RequestedProductListView.as_view()),
    path('profile/offered/', OfferedProductListView.as_view()),
    path('profile/fulfill/', FullProductView.as_view()),
    path('profile/decline/<int:pk>/', DeclineProductView.as_view()),
    path('favorite/', FavoriteProductView.as_view()),
    path('search/', SearchDetailView.as_view()),
    path('cart/', MyCartView.as_view()),
    path('report/', ReportView.as_view()),
    path('category/', GetCategoryList.as_view()),
    path('total/', PurchaseMountView.as_view()),
    path('checkout/', CheckoutProductsView.as_view()),
    path('reviewable/', ReviewableProductsView.as_view()),
    path('sendreview/', SendReview.as_view()),
    path('orders/', OrdersView.as_view()),
    path('tracking/<int:pk>/', Tracking.as_view()),
    path('webhook/', TrackingWebHook.as_view()),
    path('itemrequest/', ItemRequest.as_view()),
]
