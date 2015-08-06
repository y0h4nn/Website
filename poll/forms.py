import django.forms as forms


class PollForm(forms.Form):
    title = forms.CharField(label='Titre')
    start_time = forms.SplitDateTimeField()
    end_time = forms.SplitDateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not len(args):  # If the request is empty
            return
        questions = []
        answers = []

        # Build a list of questions and answers out of the request
        for arg in args[0]:
            if arg.startswith('q'):
                questions.append(arg)
            if arg.startswith('a'):
                answers.append(arg)

        self.questions_answers = {}
        nb_q = 1
        # Association of questions and answers
        for q in sorted(questions, key=lambda x: int(x[1:])):
            nb_a = 1
            self.questions_answers[q] = []
            self.fields[q] = forms.CharField(initial=self.data[q], label="Question " + str(nb_q))
            nb_q += 1
            for a in sorted(answers, key=lambda x: int(x[1:].split("_")[0])):
                if not a.endswith(q):
                    continue
                self.fields[a] = forms.CharField(initial=self.data[a], label="Réponse " + str(nb_a))
                self.questions_answers[q].append(a)
                nb_a += 1

    def clean(self):
        cleaned_data = super().clean()
        for q, a in self.questions_answers.items():
            if not a:
                self.add_error(q, "Vous ne pouvez pas ajouter de question sans réponse.")
