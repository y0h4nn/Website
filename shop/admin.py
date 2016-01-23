from django.contrib import admin
from .models import Product, Packs, BuyingHistory

admin.site.register(Product)
admin.site.register(Packs)
admin.site.register(BuyingHistory)
