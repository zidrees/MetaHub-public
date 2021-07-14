from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('', include('products.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    # path('targetCart/', include('targetCart.urls', namespace='targetCart')),
]
