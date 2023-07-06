from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from ads.views import AdsList, AdDetail, AdCreate, AdUpdate, AdDelete, ResponseCreate

urlpatterns = [
    path('ads/', AdsList.as_view(), name='ads_list'),
    path('ads/<int:pk>', AdDetail.as_view(), name='ad'),
    path('ads/create', AdCreate.as_view(), name='ad_create'),
    path('ads/<int:pk>/update', AdUpdate.as_view(), name='ad_update'),
    path('ads/<int:pk>/delete', AdDelete.as_view(), name='ad_delete'),
    path('ads/<int:pk>/res_create', ResponseCreate.as_view(), name='res_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)