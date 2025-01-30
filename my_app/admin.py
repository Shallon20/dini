from django.contrib import admin
from .models import Event, InterpreterApplication, Client, Profile

# Register your models here.
admin.site.register(Event)
admin.site.register(Client)
admin.site.register(InterpreterApplication)
admin.site.register(Profile)


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'date_created')
    search_fields = ('title', 'short_description')
