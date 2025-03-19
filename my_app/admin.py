from django.contrib import admin
from .models import Event, InterpreterApplication, Client, Profile, EducationalResource, Interpretation, CommunityGroup, \
    GalleryImage, FAQ


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'is_new')  #
    list_filter = ('is_new',)
    search_fields = ('title', 'short_description')

class EducationalResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'category')
    list_filter = ('category',)

class InterpreterApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

class InterpretationAdmin(admin.ModelAdmin):
    list_display = ('service_type',)


class CommunityGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform')

class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)


admin.site.register(EducationalResource, EducationalResourceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Client)
admin.site.register(InterpreterApplication, InterpreterApplicationAdmin)
admin.site.register(Profile)
admin.site.register(Interpretation)
admin.site.register(CommunityGroup, CommunityGroupAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(FAQ, FAQAdmin)
