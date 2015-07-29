from django.contrib import admin
from .models import Question, Answer, Poll

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Poll)

