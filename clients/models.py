from django.contrib.auth import get_user_model
from django.db import models
from users.models import User


User = get_user_model()

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.full_name} <{self.email}>'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'



