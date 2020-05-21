from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from reviews.models import Doctor, ExceptionWord, Review

User = get_user_model()


class TestDoctorModel(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            first_name="Ай", last_name="Болит", patronymic="Вениаминович"
        )
        self.specialty = self.doctor.spec.create(title="Therapist")
        self.doctor.spec.create(title="Neurolog")

    def test_doctor_object_name(self):
        expected_object_name = (
            f"{self.doctor.last_name} {self.doctor.first_name} {self.doctor.patronymic}"
        )
        self.assertEquals(expected_object_name, str(self.doctor))


class TestReviewModel(TestCase):
    def setUp(self):
        self.author = User.objects.create(
            username="test", email="alice@spam.eggs", password="superpassword"
        )
        self.doctor = Doctor.objects.create(
            first_name="Ай", last_name="Болит", patronymic="Вениаминович"
        )
        self.specialty = self.doctor.spec.create(title="Therapist")
        self.doctor.spec.create(title="Neurolog")
        self.review = Review.objects.create(
            author=self.author,
            doctor=self.doctor,
            ip_address="127.0.0.1",
            text="  lorem   IPSUM   DoLoR sit amet,,,,,,   CONSECTEUR adipiscing elit!!!!",
        )

    def test_review_capitalization(self):
        self.assertEquals(
            self.review.formatted_text,
            "Lorem ipsum dolor sit amet, consecteur adipiscing elit!",
        )

    def test_punctuation_formatting(self):
        self.review.text = "раз , два"
        self.assertEquals(
            self.review.format_text(), "раз, два",
        )

    def test_punctuation_repeats(self):
        self.review.text = "раз ,,,,, два!!!!"
        self.assertEquals(
            self.review.format_text(), "раз, два!",
        )

    def test_punctuation_leading(self):
        self.review.text = ",раз , два"
        self.assertEquals(
            self.review.format_text(), ",раз, два",
        )

    def test_punctuation_one_dot(self):
        self.review.text = "."
        self.assertEquals(
            self.review.format_text(), ".",
        )

    def test_punctuation_multiple_spaces(self):
        self.review.text = "раз    , два"
        self.assertEquals(
            self.review.format_text(), "раз, два",
        )
