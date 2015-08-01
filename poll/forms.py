import django.forms as forms


class PollForm(forms.Form):
    title = forms.CharField(label='Titre')
    start_time = forms.SplitDateTimeField()
    end_time = forms.SplitDateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not len(args):
            return
        questions = []
        answers = []

        for arg in args[0]:
            if arg.startswith('q'):
                questions.append(arg)
            if arg.startswith('a'):
                answers.append(arg)

        self.questions_answers = {}
        nb_q = 1
        for q in sorted(questions, key=lambda x: int(x[1:])):
            nb_a = 1
            self.questions_answers[q] = []
            self.fields[q] = forms.CharField(initial=self.data[q], label="Question " + str(nb_q))
            nb_q += 1
            for a in sorted(answers, key=lambda x: int(x[1:].split("_")[0])):
                if a.endswith(q):
                    self.fields[a] = forms.CharField(initial=self.data[a], label="Réponse " + str(nb_a))
                    self.questions_answers[q].append(a)
                    nb_a += 1
        print(self.questions_answers)
