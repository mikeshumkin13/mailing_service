from django.db import models
from django.conf import settings


class Client(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name='Владелец'
    )
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.full_name} ({self.email})'


