from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:usItemId>/', views.cart_add, name='cart_add'),
# re_path(add/(?P<house_id>[0-9]+)/$',view.cart_add)
    # path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
