from django.db import models
from django.conf import settings


class Partnership(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="partnerships/logos")
    description = models.TextField()
    address = models.CharField(max_length=300)
    urlLink = models.URLField(max_length=300)

    class Meta:
         app_label = 'partnerships'
         permissions = (
                     ('manage_partnerships', 'Can manage partnerships'),
                 )

    def __str__(self):
        return self.name
