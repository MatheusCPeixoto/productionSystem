from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from activitys.urls import urlpatterns as activitys_urls
from enterprises.urls import urlpatterns as enterprises_urls
from equipments.urls import urlpatterns as equipments_urls
from workforces.urls import urlpatterns as workforces_urls
from non_conformities.urls import urlpatterns as non_conformities_urls
from stop_reasons.urls import urlpatterns as stop_reason_urls
from production_tracking.urls import urlpatterns as production_tracking_urls
from orders.urls import urlpatterns as orders_urls
from products.urls import urlpatterns as products_urls

urlpatterns = [
    #path('jet/', include('jet.urls', 'jet')),  # URLs do Django JET
    #path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(activitys_urls)),
    path('api/v1/', include(enterprises_urls)),
    path('api/v1/', include(equipments_urls)),
    path('api/v1/', include(workforces_urls)),
    path('api/v1/', include(non_conformities_urls)),
    path('api/v1/', include(stop_reason_urls)),
    path('api/v1/', include(production_tracking_urls)),
    path('api/v1/', include(orders_urls)),
    path('api/v1/', include(products_urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

