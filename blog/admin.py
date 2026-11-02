from django.contrib import admin
from .models import Blog
from .models import Event

admin.site.register(Event)
admin.site.register(Blog)