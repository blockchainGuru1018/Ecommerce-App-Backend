from django.urls import path

from .views import login_view, logout_view, user_list_view, product_list_view, user_detail_view, user_edit_view, \
    user_add_view, user_delete_view, product_detail_view, product_edit_view, product_add_view, product_delete_view, \
    transaction_list_view, transaction_add_view, transaction_detail_view, transaction_edit_view, \
    transaction_delete_view, report_list_view

app_name = 'authorize'

urlpatterns = [
    path('', user_list_view),
    path('user-add/', user_add_view),
    path('user-detail/<int:pk>/', user_detail_view),
    path('user-update/<int:pk>/', user_edit_view),
    path('user-delete/<int:pk>', user_delete_view),
    path('products-list', product_list_view),
    path('product-add/', product_add_view),
    path('product-detail/<int:pk>/', product_detail_view),
    path('product-update/<int:pk>/', product_edit_view),
    path('product-delete/<int:pk>', product_delete_view),
    path('transactions-list', transaction_list_view),
    path('transaction-add/', transaction_add_view),
    path('transaction-detail/<int:pk>/', transaction_detail_view),
    path('transaction-update/<int:pk>/', transaction_edit_view),
    path('transaction-delete/<int:pk>', transaction_delete_view),
    path('report-list', report_list_view),
    path('login/', login_view),
    path('logout/', logout_view),
]
