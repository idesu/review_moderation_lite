import re

from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(default='')
    formatted_text = models.TextField()
    created = models.DateTimeField('creation date', auto_now_add=True, db_index=True)

    def format_text(self):
        clean_repeated_puncts = re.sub(r'([.\?#,<>%~`!$:;])\1+', r'\1', self.text)
        fix_spaces = re.sub(' +', ' ', clean_repeated_puncts)
        formatted_text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', fix_spaces)
        # capitalize text if finded >6 uppercase chars in a row
        if re.search(r'([A-ZА-Я]{6})', fix_spaces):
            formatted_text = re.sub(r"(\A\w)|"+     # start of string
                "(?<!\.\w)([\.?!] )\w|"+            # after a ?/!/. and a space, 
                                                    # but not after an acronym
                "\w(?:\.\w)|"+                      # start/middle of acronym
                "(?<=\w\.)\w",                      # end of acronym
                lambda x: x.group().upper(), 
                fix_spaces.lower())
        return formatted_text

@receiver(models.signals.post_save, sender=Review)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.formatted_text = instance.format_text()



class Fword(models.Model):
    word = models.CharField('f-word', max_length=150)


class ExceptionWord(models.Model):
    word = models.CharField('exception word', max_length=150)
