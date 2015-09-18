from django import forms
from .models import Pizza, Command
from django.utils import timezone


class PizzaAddingForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name']
        labels = {'name': "Nom"}

class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['date']
        widgets = {"date": forms.SplitDateTimeWidget()}

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        if not date:
            return cleaned_data
        current = Command.get_current()
        if current is not None and not current.is_valid():
            if date < current.date:
                self.add_error("date", "Vous ne pouvez pas avoir une commande plus vieille que la derniere commande")
        if date < timezone.now():
            self.add_error("date", "Impossible d'avoir une commande dans le passé")
        return cleaned_data

class PizzaTakingForm(forms.Form):
    pizza = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        pizzas = kwargs.pop('pizzas')
        super().__init__(*args, **kwargs)
        self.fields['pizza'].choices = [(pizza.id, str(pizza)) for pizza in pizzas]

