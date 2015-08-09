import django.forms as forms
import json


class QuestionWidget(forms.widgets.TextInput):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qid = parent.qid
        self.answers = parent.answers
        self.data = parent.data

    def render(self, name="", value="", **kwargs):
        plus = "<button onclick=\"add_response({qid});return false;\">+</button><button onclick=\"del_question({qid});return false;\">x</button><div id=\"q_a{real_qid}\"></div>"
        plus += "<div id=\"q_a{qid}\">"
        for i, answer in enumerate(self.answers):
            plus += "<div id=\"div_q" + self.qid[1:] + "_" + str(i + 1) + "\"><label for=\""+ answer +"\">Réponse: </label>" + super().render(name=answer, value=self.data[answer], attrs={"id": answer}) + "<button onclick=\"del_answer(" + self.qid[1:] + "," + str(i + 1) + ");return false;\">x</button></div>"
        plus += "</div></fieldset>"
        return "<fieldset id=\"div_q" + self.qid[1:] + "\"><label for=\"" + self.qid + "\">Question: </label>" + super().render(name=name, value=value, **kwargs) + plus.format(qid=self.qid[1:], real_qid=self.qid)


class QuestionField(forms.Field):
    def __init__(self, qid, answers, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qid = str(qid)
        self.answers = answers
        self.data = data
        self.widget = QuestionWidget(self)


class PollForm(forms.Form):
    title = forms.CharField(label='Titre')
    start_time = forms.SplitDateTimeField()
    end_time = forms.SplitDateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q_a_nb = "{}"
        self.questions_answers = {}
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

        nb_q = 1
        # Association of questions and answers
        for q in sorted(questions, key=lambda x: int(x[1:])):
            nb_a = 1
            self.questions_answers[q] = []
            for a in sorted(answers, key=lambda x: int(x[1:].split("_")[0])):
                if not a.endswith(q):
                    continue
                self.questions_answers[q].append(a)
                nb_a += 1
            self.fields[q] = QuestionField(qid=q, answers=self.questions_answers[q], data=self.data, initial=self.data[q], label="Question " + str(nb_q))
            nb_q += 1
        self.q_a_nb = json.dumps({q[1:]: len(a) for q, a in self.questions_answers.items()})

    def clean(self):
        cleaned_data = super().clean()
        for q, a in self.questions_answers.items():
            if not a:
                self.add_error(None, "Vous ne pouvez pas ajouter de question sans réponse.")
            for answer in a:
                cleaned_data[answer] = forms.CharField(required=False).clean(self.data[answer])
                if not cleaned_data[answer]:
                    self.add_error(None, "Vous ne pouvez pas avoir de réponse vide")

