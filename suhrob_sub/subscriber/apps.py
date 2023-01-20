from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscriberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'suhrob_sub.subscriber'
    verbose_name = _('Subscriber')

    def ready(self):
        from suhrob_sub.subscriber.subscriber import subscriber
        subscriber.start()
