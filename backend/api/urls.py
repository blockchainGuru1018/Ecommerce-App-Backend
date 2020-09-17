from django.urls import path, re_path, include

from .views import UserLoginView, SocialLoginView, UserRegistrationView, \
    ForgotPasswordView, ConfirmTokenView, ResetPasswordView, UserLogoutView, CategoryProductsView, NewestProductsView, PopularProductsView, ChangePasswordView

app_name = 'api'

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('social-login/', SocialLoginView.as_view()),
    path('register/', UserRegistrationView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('confirm-token/', ConfirmTokenView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('home/products-by-category/', CategoryProductsView.as_view()),
    path('home/newest-products/', NewestProductsView.as_view()),
    path('home/popular-products/', PopularProductsView.as_view()),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^products/', include('products.urls')),
]
