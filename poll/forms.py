import django.forms as forms
import json


class QuestionWidget(forms.widgets.TextInput):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qid = parent.qid
        self.answers = parent.answers
        self.data = parent.data

    def render(self, name="", value="", **kwargs):
        plus = "<button onclick=\"add_response({qid});return false;\"><i class=\"fa fa-plus\"></i></button><button class=\"red_button\" onclick=\"del_question({qid});return false;\"><i class=\"fa fa-trash-o\"></i></button></p><div id=\"q_a{real_qid}\"></div>"
        plus += "<div id=\"q_a{qid}\">"
        for i, answer in enumerate(self.answers):
            plus += "<div id=\"div_q" + self.qid[1:] + "_" + str(i + 1) + "\"><p><label for=\""+ answer +"\">Réponse: </label>" + super().render(name=answer, value=self.data[answer], attrs={"id": answer}) + "<button class=\"red_button\" onclick=\"del_answer(" + self.qid[1:] + "," + str(i + 1) + ");return false;\"><i class=\"fa fa-minus\"></i></button></p></div>"
        plus += "</div></fieldset>"
        return "<fieldset id=\"div_q" + self.qid[1:] + "\"><p><label for=\"" + self.qid + "\">Question: </label>" + super().render(name=name, value=value, **kwargs) + plus.format(qid=self.qid[1:], real_qid=self.qid)


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
    group = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['group'].choices = [(x, x) for x in user.groups.all()]
        self.q_a_nb = "{}"
        self.questions_answers = {}
        for f in ['start_time', 'end_time']:
            self.fields[f].widget.widgets[0].attrs['placeholder'] = "DD/MM/YYYY"
            self.fields[f].widget.widgets[1].attrs['placeholder'] = "HH:MM"
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
        err_no_answer = False
        err_empty_answer = False
        err_empty_question = False
        if not self.questions_answers:
            self.add_error(None, "Il doit y avoir au moins une question")
        for q, a in self.questions_answers.items():
            if not a and not err_no_answer:
                err_no_answer = True
                self.add_error(None, "Vous ne pouvez pas ajouter de question sans réponse.")
            if not self.data[q] and not err_empty_question:
                err_empty_question = True
                self.add_error(None, "Vous ne pouvez pas avoir de question vide")
            for answer in a:
                cleaned_data[answer] = forms.CharField(required=False).clean(self.data[answer])
                if not cleaned_data[answer] and not err_empty_answer:
                    err_empty_answer = True
                    self.add_error(None, "Vous ne pouvez pas avoir de réponse vide")
        if cleaned_data.get('start_time') and cleaned_data.get('end_time'):
            if cleaned_data['start_time'] >= cleaned_data['end_time']:
                self.add_error('start_time', "Le début du sondage doit etre avant la fin")

