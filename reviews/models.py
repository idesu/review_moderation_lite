from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Specialty(models.Model):
    title = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Doctor(models.Model):
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    patronymic = models.CharField('patronymic', max_length=150, blank=True)
    spec = models.ManyToManyField(Specialty)

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    created = models.DateTimeField('creation date', auto_now_add=True, db_index=True)  


class Fword(models.Model):
    word = models.CharField('f-word', max_length=150)

class ExceptionWord(models.Model):
    word = models.CharField('exception word', max_length=150)
