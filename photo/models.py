from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)
    parent = models.ForeignKey('Album', null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    @staticmethod
    def get_childs(album):
        return Album.objects.filter(parent=album)

class Photo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)
    album = models.ForeignKey(Album)
    image = models.ImageField(height_field="height", width_field="width")

    def __str__(self):
        return self.name

