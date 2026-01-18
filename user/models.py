from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User (AbstractUser):
    username = models.CharField(max_length=125, verbose_name= 'Псевдоним')
    first_name = models.CharField(max_length=125, blank = True, null = True, verbose_name= 'Имя')
    last_name = models.CharField(max_length=125, blank= True, null= True, verbose_name= 'Фамилия')
    email = models.EmailField(unique= True, verbose_name= 'Почта')
    phone  = models.CharField(max_length=20, blank= True, null= True,  verbose_name= 'Телефон')
    password = models.CharField(max_length=125, verbose_name= 'Пароль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return f'{self.username} : {self.email}'