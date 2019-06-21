from django import forms
from web.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file', 'is_active')
