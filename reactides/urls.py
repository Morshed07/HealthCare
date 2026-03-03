from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.core.urls')),
    path('api/account/', include('apps.account.urls')),
    path('api/representative/', include('apps.representative.urls')),
    path('api/products/', include('apps.product.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/checkout/', include('apps.checkout.urls')),
    



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
