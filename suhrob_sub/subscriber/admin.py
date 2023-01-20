from django.contrib import admin
from suhrob_sub.subscriber.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'en', 'ru', 'date')
    search_fields = ('en', 'ru', 'date')
    readonly_fields = ('en', 'ru', 'date')
