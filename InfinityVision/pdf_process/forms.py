from django import forms

from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']


class EditDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['original_name']
