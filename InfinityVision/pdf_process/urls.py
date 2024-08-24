from django.urls import path

from . import views

app_name = 'pdf_process'

urlpatterns = [
    path('my_pdfs/', views.my_pdfs, name='my_pdfs'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('upload/success/', views.upload_success, name='upload_success'),
]
