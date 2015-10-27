from django.shortcuts import render
from .models import Note, Category, PriceDescription, Product, Price, HistoryLine
from django.http import Http404, HttpResponse
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
        req = get_req_or_404(request)
        id_ = req.pop('id')
        if request.method == "PUT":
            create_or_update(cls, id_, **req)
        elif request.method == "DELETE":
            cls.objects.get(foreign_id=id_).delete()
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

