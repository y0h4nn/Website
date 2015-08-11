from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, Poll, Voter
from .forms import PollForm


@login_required()
def question(request, pid):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    p = get_object_or_404(Poll, id=pid)
    context = {'poll': p, 'pid': pid, "errors": []}
    if not p.is_open():
        if p.is_ended():
            return render(request, 'poll/results.html', context)
        return redirect(reverse('poll:index'))

    try:
        already_voted = Voter.objects.get(user=request.user, poll=p)
    except Voter.DoesNotExist:
        pass
    else:
        return redirect(reverse('poll:already'))

    answers = {q.id: request.POST.get("question{}".format(q.id), None) for q in p.questions.all()}

    if all(answers.values()):
        if any(int(Answer.objects.get(id=aid).question.id) != int(qid) for qid, aid in answers.items()):
            context["errors"].append("Nope")  # This should NEVER happen
            return render(request, 'poll/question.html', context)
        for aid in answers.values():
            Answer.objects.filter(id=aid).update(votes=F("votes") + 1)
        v = Voter(user=request.user, poll=p)
        v.save()
        return redirect(reverse('poll:thanks'))
    else:
        context["errors"].append("Veuillez répondre à toutes les questions")
    return render(request, 'poll/question.html', context)


@login_required()
def thanks(request):
    return render(request, 'poll/thanks.html', {})


@login_required()
def already(request):
    return render(request, 'poll/already.html', {})


@login_required()
def poll_index(request):
    context = {'polls': Poll.objects.filter(group__in=request.user.groups.all())}
    return render(request, 'poll/index.html', context)


@login_required()
def admin_index(request):
    context = {'polls': Poll.objects.filter(group__in=request.user.groups.all())}
    return render(request, 'poll/admin/index.html', context)


@login_required()
def admin_add_poll(request):
    if request.method == 'GET':
        form = PollForm(user=request.user)
    elif request.method == 'POST':
        form = PollForm(request.POST, user=request.user)

        if form.is_valid():
            if not request.user.groups.filter(name=form.cleaned_data['group']).count():
                return render(request, 'poll/admin/add.html', {'form': form})
            g = request.user.groups.get(name=form.cleaned_data['group'])
            p = Poll(title=form.cleaned_data['title'], author=request.user, start_date=form.cleaned_data['start_time'], end_date=form.cleaned_data['end_time'], group=g)
            p.save()
            for question, answers in form.questions_answers.items():
                q = Question(poll=p, text=form.cleaned_data[question])
                q.save()
                for answer in answers:
                    a = Answer(question=q, text=form.cleaned_data[answer], votes=0)
                    a.save()
            return redirect(reverse('poll:admin'))
    else:
        return HttpResponseNotAllowed()
    return render(request, 'poll/admin/add.html', {'form': form})

