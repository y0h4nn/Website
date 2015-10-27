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


def request_note(request):
    note = get_req_or_404(request)
    note_id = note.pop('id')

    if request.method == "PUT":
        create_or_update(Note, note_id, **note)
    elif request.method == "DELETE":
        Note.objects.get(foreign_id=note_id).delete()
    else:
        raise Http404
    return HttpResponse(200)


def request_category(request):
    category = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404
    return HttpResponse(200)


def request_price_description(request):
    price_description = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404
    return HttpResponse(200)


def request_product(request):
    product = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404
    return HttpResponse(200)


def request_price(request):
    price = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404
    return HttpResponse(200)


def request_history_line(request):
    history_line = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404
    return HttpResponse(200)

