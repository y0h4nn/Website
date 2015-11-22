from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from events.models import Event, Inscription
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


class RegistrationSerializer(serializers.BaseSerializer):
    count = serializers.IntegerField()


class EventSerializer(serializers.HyperlinkedModelSerializer):
    places_left = serializers.IntegerField(
        source='nb_places_left',
        read_only=True
    )

    class Meta:
        model = Event
        fields = [
            'id',
            'url',
            'name',
            'end_inscriptions',
            'start_time',
            'end_time',
            'location',
            'description',
            'price',
            'limited',
            'max_inscriptions',
            'places_left',
            'allow_extern',
            'allow_invitations',
            'max_invitations',
            'max_invitations_by_person',
        ]

        # Do not bother adding places_left as readonly here, it does not work
        read_only_fields = [
            'id',
            'url',
            'name',
            'end_inscriptions',
            'start_time',
            'end_time',
            'location',
            'description',
            'price',
            'limited',
            'max_inscriptions',
            'allow_extern',
            'allow_invitations',
            'max_invitations',
            'max_invitations_by_person',
        ]


class EventViewSet(viewsets.ModelViewSet):
    """
    ## Managing event registration

    ### Register user to event with id 1

        /api/events/1/set_registration/

    with the following POST data

        {
            "registration": Boolean
        }

    user who perform the request will then be added to/removed from the event
    registered users

    ### Get user registration for event with id 1

        /api/events/1/get_registration/

    -------
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @detail_route(methods=['POST'])
    def set_registration(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if self.request.data.get('registration') == False:
            try:
                ins = Inscription.objects.get(event=event, user=request.user)
                ins.delete()
            except Inscription.DoesNotExist:
                pass
        else:
            try:
                ins = Inscription.objects.create(event=event, user=request.user)
            except IntegrityError:
                pass

        return Response({})

    @detail_route()
    def get_registration(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        registered = False
        try:
            Inscription.objects.get(event=event, user=request.user)
            registered = True
        except Inscription.DoesNotExist:
            pass
        return Response({'user_is_registered': registered})
