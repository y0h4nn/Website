import django.forms as forms


class PollForm(forms.Form):
    title = forms.CharField(label='Titre')
    start_time = forms.DateTimeField(widget=forms.widgets.SplitDateTimeWidget)
    end_time = forms.DateTimeField(widget=forms.widgets.SplitDateTimeWidget)

    q1 = forms.CharField(label='Question 1')
    a1_q1 = forms.CharField(label='Réponse 1')
    a2_q1 = forms.CharField(label='Réponse 2')

