from django import forms
from .models import Pizza

class PizzaAddingForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name']
        labels = {'name': "Nom"}


class PizzaTakingForm(forms.Form):
    pizza = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        pizzas = kwargs.pop('pizzas')
        super().__init__(*args, **kwargs)
        self.fields['pizza'].choices = [(pizza.id, str(pizza)) for pizza in pizzas]

