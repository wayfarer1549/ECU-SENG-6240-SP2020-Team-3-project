from django import forms
from . import models

class CreateContract(forms.ModelForm):
    class Meta:
        model = models.Contract
        fields = ['title', 'body', 'slug']
        