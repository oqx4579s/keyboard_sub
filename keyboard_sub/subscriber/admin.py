from django.contrib import admin
from keyboard_sub.subscriber.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'en', 'ru', 'date', 'favorite', 'note')
    search_fields = ('en', 'ru', 'date')
    list_filter = ('favorite', )
    readonly_fields = ('en', 'ru', 'date')
    fieldsets = (
        (None, {
            'fields': ('en', 'ru', 'date'),
        }),
        (None, {
            'fields': ('favorite', 'note'),
        }),
    )
