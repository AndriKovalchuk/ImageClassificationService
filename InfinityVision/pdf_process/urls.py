from django.urls import path

from . import views

app_name = 'pdf_process'

urlpatterns = [
    path('my_documents/', views.my_documents, name='my_documents'),
    path('upload/', views.upload_document, name='upload_document'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('edit/<int:document_id>/', views.edit_document_view, name='edit_document_view'),
    path('edit_name/<int:document_id>/', views.edit_document_name, name='edit_document_name'),
    path('delete/<int:document_id>', views.delete_document, name='delete_document'),
]
