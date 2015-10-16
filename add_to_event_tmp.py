from django.contrib.auth.models import User
from events.models import Event, Inscription

e = Event.objects.get(id=32)
for obj in User.objects.all():
    print(obj, e)
    try:
        i = Inscription.objects.create(user=obj, event=e)
    except:
        print(obj, "failed")
