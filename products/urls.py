from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # post views
    path('', views.product_search, name='product_search'),
    path('product/<str:category_slug>/', views.ProductListView.as_view(), name='product_list_search'),
]
