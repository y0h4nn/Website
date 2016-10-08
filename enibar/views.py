from .models import Note, HistoryLine
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
import datetime
import os.path
import json


def get_req_or_404(request):
    try:
        return json.loads(request.read().decode())
    except json.JSONDecodeError:
        raise Http404


def check_token(request):
    if 'token' not in request:
        raise PermissionDenied
    token = request.pop('token')
    if token != settings.AUTH_SYNC_ENIBAR_TOKEN:
        raise PermissionDenied


def create_or_update(cls, foreign_id, **kwargs):
    try:
        obj = cls.objects.get(foreign_id=foreign_id)
    except cls.DoesNotExist:
        cls.objects.create(foreign_id=foreign_id, **kwargs)
    else:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()


def _create_view(cls):
    @csrf_exempt
    def view(request):
        if request.method == "PUT":
            req = get_req_or_404(request)
            check_token(req)
            id_ = req.pop('id')
            create_or_update(cls, id_, **req)
        elif request.method == "DELETE":
            req = get_req_or_404(request)
            check_token(req)
            id_ = req.pop('id')
            try:
                cls.objects.get(foreign_id=id_).delete()
            except:
                return HttpResponse(200)
        elif request.method == "GET":
            try:
                get = {key: value for key, value in request.GET.items()}
                res = [obj['fields'] for obj in json.loads(serializers.serialize("json", cls.objects.filter(**get)))]
                return JsonResponse(res, safe=False)
            except:  # Whaterver...
                raise Http404
        else:
            raise Http404
        return HttpResponse(200)
    return view


request_note = _create_view(Note)
request_history = _create_view(HistoryLine)


def show_history(request, page):
    page = page or 1
    note = get_object_or_404(Note, mail=request.user.email)
    paginator = Paginator(HistoryLine.objects.filter(note=note.nickname).order_by('-id'), 50)

    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)

    context = {"history": history}

    return render(request, 'enibar/history.html', context)

def get_photo_paths(request):
    last_updated = request.GET.get('last_updated')
    if last_updated:
        last_updated = datetime.datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S")
        users = User.objects.filter(profile__last_updated__gt=last_updated).select_related('profile')
    else:
        users = User.objects.all().select_related('profile')
    photos = {user.email: os.path.basename(user.profile.picture.path) for user in users if user.profile.picture and user.email}

    return JsonResponse(photos, safe=False)
