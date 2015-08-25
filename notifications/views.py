from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from . import models


def index(request):
    context = {
        'notifications': models.Notification.objects.filter(user=request.user,read=False).order_by('date').all().reverse()
    }

    return render(request, 'notifications/index.html', context)

def read(request, nid):
    notification = get_object_or_404(models.Notification, id=nid, user=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({'status': 'ok'})
