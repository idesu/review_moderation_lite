from django.forms import ModelForm
from django import forms
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 100:
            raise forms.ValidationError("Должно быть хотя бы 100 символов")
        return text
