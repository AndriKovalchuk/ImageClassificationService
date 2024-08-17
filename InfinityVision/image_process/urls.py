from django.urls import path
from . import views

app_name = 'image_process'

urlpatterns = [
    path('my_images/', views.my_images, name='my_images'),
    path('upload/', views.upload_image, name='upload_image'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('classify/<int:image_id>/', views.classify_image_view, name='classify_image'),
]
