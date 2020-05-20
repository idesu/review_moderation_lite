# -*- coding: utf-8 -*-
import re

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.db import models

User = get_user_model()


class Specialty(models.Model):
    title = models.CharField("Специальность", max_length=200)

    class Meta:
        ordering = ["title"]
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"

    def __str__(self):
        return self.title


class Doctor(models.Model):
    first_name = models.CharField("Имя", max_length=30, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    patronymic = models.CharField("Отчество", max_length=150, blank=True)
    spec = models.ManyToManyField(Specialty)

    class Meta:
        verbose_name = "Врача"
        verbose_name_plural = "Врачи"

    @property
    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    @property
    def get_spec(self):
        return ", ".join(spec.title for spec in self.spec.all())

    def get_absolute_url(self):
        return reverse('new_review', args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", blank=True, null=True
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    ip_address = models.GenericIPAddressField()
    text = models.TextField("Текст отзыва", default="")
    formatted_text = models.TextField("Форматированный текст",)
    dt_created = models.DateTimeField("Дата создания", auto_now_add=True)
    dt_updated = models.DateTimeField("Дата последнего обновления", auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def format_text(self):
        clean_repeated_puncts = re.sub(r"([.\?#,<>%~`!$:;])\1+", r"\1", self.text)
        fix_spaces = re.sub(" +", " ", clean_repeated_puncts)
        formatted_text = re.sub(r'\s([?.!"](?:\s|$))', r"\1", fix_spaces)
        # capitalize text if finded >6 uppercase chars in a row
        if re.search(r"([A-ZА-Я]{6})", formatted_text):
            formatted_text = re.sub(
                r"(\A\w)|"
                + "(?<!\.\w)([\.?!] )\w|"       # start of string
                +                               # after a ?/!/. and a space,
                                                # but not after an acronym
                "\w(?:\.\w)|"                   # start/middle of acronym
                + "(?<=\w\.)\w",                # end of acronym
                lambda x: x.group().upper(),
                formatted_text.lower(),
            )
        return formatted_text

    def save(self, *args, **kwargs):
        if self.id is None:
            self.formatted_text = self.format_text()
        super().save(*args, **kwargs)


class Fword(models.Model):
    word = models.CharField("Слово", max_length=150)

    class Meta:
        verbose_name = "Ругательство"
        verbose_name_plural = "Ругательства"
    
    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.word


class ExceptionWord(models.Model):
    word = models.CharField("Слово", max_length=150)

    class Meta:
        verbose_name = "Слово-исключение"
        verbose_name_plural = "Слова-исключения"

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.word
