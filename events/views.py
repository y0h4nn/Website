from django.shortcuts import render
from .models import Event
from .forms import EventForm


def event(request, eid):
    return render(request, 'events/event.html')

def admin_index(request):
    context = {'events': Event.objects.all()}
    return render(request, 'events/admin/index.html', context)

def admin_add(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EventForm()
    context = {'event_form': form}
    return render(request, 'events/admin/add.html', context)

