from django.urls import path

from . import views

app_name = 'image_process'

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('success/', views.upload_success, name='upload_success'),
    path('my-images/', views.my_images, name='my_images'),
    path('classify/<int:image_id>/', views.classify_image_view, name='classify_image'),
    path('edit/<int:image_id>/', views.edit_image_name, name='edit_image_name'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
]
