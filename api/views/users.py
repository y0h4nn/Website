from rest_framework import serializers, viewsets
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
            'picture',
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
    """
    **Readonly** api to gather user informations.
    """
    queryset = User.objects.prefetch_related('profile').all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    class Meta:
        methods = ['GET']

