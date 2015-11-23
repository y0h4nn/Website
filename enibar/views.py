from .models import Note, HistoryLine
from django.conf import settings
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
            cls.objects.get(foreign_id=id_).delete()
        elif request.method == "GET":
            try:
                get = {key: value[0] for key, value in request.GET.items()}
                res = [obj['fields'] for obj in json.loads(serializers.serialize("json", cls.objects.filter(**get)))]
                return JsonResponse(res, safe=False)
            except: # Whaterver...
                raise Http404
        else:
            raise Http404
        return HttpResponse(200)
    return view


request_note = _create_view(Note)
request_history = _create_view(HistoryLine)

