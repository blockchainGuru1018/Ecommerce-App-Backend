from django.urls import path
from .views import UserDetailView, UserSettingUpdate, UsersShippingView, FollowView, UserSettingView, UserPaymentView, UserCardDeleteView, \
    BankdeleteView, BankFavoriteView, BankAddView

app_name = 'users'

urlpatterns = [
    path('', UserSettingUpdate.as_view()),
    path('me/', UserSettingView.as_view()),
    path('me/payment/', UserPaymentView.as_view()),
    path('me/payment/<int:pk>/', UserCardDeleteView.as_view()),
    path('me/bank/add/', BankAddView.as_view()),
    path('me/bank/favorite/', BankFavoriteView.as_view()),
    path('me/bank/delete/', BankdeleteView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('setting/shipping/', UsersShippingView.as_view()),
    path('following/', FollowView.as_view()),
    # path('sellers/', SellersView.as_view()),
]
