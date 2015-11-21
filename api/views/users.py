from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from django.contrib.auth.models import User
from accounts.models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='__str__')
    class Meta:
        model = Profile
        fields = [
            'nickname',
            'display_name',
            'phone',
            'birthdate',
        ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.prefetch_related('profile').all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    class Meta:
        methods = ['GET']
