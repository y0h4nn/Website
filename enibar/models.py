from django.db import models


class Note(models.Model):
    foreign_id = models.IntegerField(unique=True, db_index=True)
    nickname = models.CharField(max_length=255)
    mail = models.EmailField()
    note = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def get_note(cls, user):
        try:
            return cls.objects.get(mail=user.email)
        except cls.DoesNotExist:
            return None


class HistoryLine(models.Model):
    foreign_id = models.IntegerField(db_index=True)
    date = models.DateTimeField(default=None, null=True, blank=True)
    note = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    price_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    liquid_quantity = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def normalized_product_name(self):
        return self.product.replace('&', '')

