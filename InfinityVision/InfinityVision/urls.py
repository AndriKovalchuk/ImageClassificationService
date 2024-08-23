from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'InfinityVision'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('image_process/', include('image_process.urls')),
    path('users/', include('users.urls')),
    path('about/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
