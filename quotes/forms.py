from django.forms import ModelForm
from .models import Prof, Quote


class ProfForm(ModelForm):
    class Meta:
        model = Prof
        fields = '__all__'


class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        exclude = ['approved', 'author']
