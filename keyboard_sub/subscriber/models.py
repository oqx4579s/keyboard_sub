from django.db import models
from django.utils.translation import gettext_lazy as _


class Log(models.Model):
    en = models.TextField(blank=True)
    ru = models.TextField(blank=True)
    date = models.DateTimeField(verbose_name=_('Date'))
    favorite = models.BooleanField(default=False, verbose_name=_('Favorite'))
    note = models.TextField(blank=True, verbose_name=_('Note'))

    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')

    def __str__(self):
        return f'Log [{self.date.strftime("%Y-%m-%d %H:%M:%S")}]'
