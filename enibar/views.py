from .models import Note, Category, PriceDescription, Product, Price, HistoryLine
from .serializers import NoteSerializer
from rest_framework import routers, serializers, viewsets, status, response


class CreateOrUpdateModelViewSet(viewsets.ModelViewSet):
    def create(self, request):
        cls = self.queryset.model
        data = request.data
        try:
            obj = cls.objects.get(nickname=data['nickname'])
        except cls.DoesNotExist:
            cls.objects.create(**data)
        else:
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()


        serializer = self.serializer_class(obj)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class NoteViewSet(CreateOrUpdateModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

