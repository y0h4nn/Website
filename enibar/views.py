from django.shortcuts import render
from .models import Note, Category, PriceDescription, Product, Price, HistoryLine
from django.http import Http404, HttpResponse
import json


def get_req_or_404(request):
    try:
        return json.loads(request.read().decode())
    except json.JSONDecodeError:
        raise Http404


def request_note(request):
    note = get_req_or_404(request)

    if request.method == "PUT":
        note_id = note.pop('id')
        try:
            note_obj = Note.objects.get(foreign_id=note_id)
        except Note.DoesNotExist:
            Note.objects.create(foreign_id=note_id, **note)
        else:
            for key, value in note.items():
                setattr(note_obj, key, value)
            note_obj.save()
    elif request.method == "DELETE":
        note_obj = Note.objects.get(foreign_id=note['id'])
        note_obj.delete()
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


def request_price_description(request):
    price_description = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404


def request_product(request):
    product = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404


def request_price(request):
    price = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404


def request_history_line(request):
    history_line = get_req_or_404(request)

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        raise Http404

