from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F, Q
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import json
from .models import Question, Answer, Poll, Voter
from .forms import PollForm
from bde.shortcuts import bde_member


@bde_member
def admin_question(request, pid):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    p = get_object_or_404(Poll, id=pid)
    context = {'poll': p, 'pid': pid, "errors": []}
    return render(request, 'poll/admin/results.html', context)

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
    return render(request, 'poll/index.html')


@login_required
def poll_list(request):
    if request.method == "OPTIONS":
        return JsonResponse({'polls': [
                {
                    'title': p.title,
                    'icon': 'fa fa-pie-chart',
                    'id': p.id,
                    'start': p.start_date.strftime("%d %B %Y %H:%M"),
                    'end': p.end_date.strftime("%d %B %Y %H:%M"),
                } for p in Poll.objects.filter(Q(group__in=request.user.groups.all()) & Q(start_date__lt=timezone.now())).order_by('-end_date')]
        })


@bde_member
def admin_delete(request):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        poll = get_object_or_404(Poll, id=req['pid'])
        poll.delete()
        return JsonResponse({'status': 1})


@bde_member
def admin_index(request):
    context = {'polls': Poll.objects.filter(author=request.user)}
    return render(request, 'poll/admin/index.html', context)


@bde_member
def admin_list(request):
    return JsonResponse({'polls': [
            {
                'title': p.title,
                'icon': 'fa fa-pie-chart',
                'id': p.id,
                'start': p.start_date.strftime("%d %B %Y %H:%M"),
                'end': p.end_date.strftime("%d %B %Y %H:%M"),
                'deleted': False,
            } for p in Poll.objects.filter(author=request.user).order_by('-end_date')
        ]
    })


@bde_member
def admin_add_poll(request):
    if request.method == 'GET':
        form = PollForm(user=request.user)
    elif request.method == 'POST':
        form = PollForm(request.POST, user=request.user)

        if form.is_valid():
            g = form.cleaned_data['group']
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


@bde_member
def admin_edit_poll(request, pid):
    if request.method == 'GET':
        p = get_object_or_404(Poll, id=pid)
        initial_q_a = {question: [answer for answer in question.answers.all()] for question in p.questions.all()}
        form = PollForm(user=request.user, initial_q_a=initial_q_a, instance=p)
        form.fields['title'].initial = p.title
        form.fields['start_time'].initial = p.start_date
        form.fields['end_time'].initial = p.end_date
        form.fields['group'].initial = p.group
    elif request.method == 'POST':
        p = get_object_or_404(Poll, id=pid)
        form = PollForm(request.POST, user=request.user, instance=p)
        if form.is_valid():
            p.title = form.cleaned_data['title']
            p.start_date = form.cleaned_data['start_time']
            p.end_date = form.cleaned_data['end_time']
            p.group = form.cleaned_data['group']

            for fq, (question, answers) in zip(p.questions.all(), form.questions_answers.items()):
                fq.text = form.cleaned_data[question]
                fq.save()
                for fa, answer in zip(fq.answers.all(), answers):
                    fa.text = form.cleaned_data[answer]
                    fa.save()
            p.save()

    return render(request, 'poll/admin/edit.html', {'form': form, 'pid': pid, 'edit_mode': True})

