import random
import string

import factory
from django.contrib.auth import get_user_model

from reviews.models import Doctor, Review, Specialty

User = get_user_model()


def random_string(length=10):
    return u"".join(random.choice(string.ascii_letters) for x in range(length))


class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "reviews.Doctor"

    first_name = "Ай"
    last_name = "Болит"
    patronymic = "Вениаминович"


class SpecFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "reviews.Specialty"

    title = factory.LazyAttribute(lambda t: random_string())


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda t: random_string())
    email = "alice@spam.eggs"
    password = "superpassword"


class ReviewFactory(factory.DjangoModelFactory):
    class Meta:
        model = "reviews.Review"

    author = factory.SubFactory(UserFactory)
    doctor = factory.SubFactory(DoctorFactory)
    ip_address = "127.0.0.1"
    text = factory.LazyAttribute(lambda t: random_string())
