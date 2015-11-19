from rest_framework import serializers, viewsets
from events.models import Event

class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'end_inscriptions',
            'start_time',
            'end_time',
            'location',
            'description',
            'price',
            'private',
            'limited',
            'max_inscriptions',
            'allow_extern',
            'allow_invitations',
            'max_invitations',
            'max_invitations_by_person',
            'gestion',
        ]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer



