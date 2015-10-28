from rest_framework import routers, serializers, viewsets
from .models import Note

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'nickname', 'mail', 'note')

