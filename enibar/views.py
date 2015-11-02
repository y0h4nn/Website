from django.shortcuts import render
from django.core import serializers
from .models import Note, Category, PriceDescription, Product, Price, HistoryLine
from django.http import Http404, HttpResponse, JsonResponse
import json


def get_req_or_404(request):
    try:
        return json.loads(request.read().decode())
    except json.JSONDecodeError:
        raise Http404


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
    def view(request):
        if request.method == "PUT":
            req = get_req_or_404(request)
            id_ = req.pop('id')
            create_or_update(cls, id_, **req)
        elif request.method == "DELETE":
            req = get_req_or_404(request)
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
request_category = _create_view(Category)
request_price_description = _create_view(PriceDescription)
request_product = _create_view(Product)
request_price = _create_view(Price)
request_history = _create_view(HistoryLine)
