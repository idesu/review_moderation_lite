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

    def test_doctor_get_full_name(self):
        expected_full_name = f"{self.doctor.last_name} {self.doctor.first_name} {self.doctor.patronymic}"
        self.assertEqual(self.doctor.get_full_name, expected_full_name)

    def test_doctor_object_name_is_last_name_comma_first_name(self):
        expected_object_name = f"{self.doctor.last_name} {self.doctor.first_name} {self.doctor.patronymic}"
        self.assertEquals(expected_object_name,str(self.doctor))

    def test_doctor_get_absolute_url(self):
        self.assertEquals(self.doctor.get_absolute_url(),'/add-review/1/')

    def test_doctor_get_spec(self):
        self.assertEquals(self.doctor.get_spec, ", ".join(spec.title for spec in self.doctor.spec.all()))

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
    
    def test_review_formatted_text(self):
        self.review = Review.objects.create(author=self.author, doctor=self.doctor, ip_address = '127.0.0.1', text='Lorem   IPSUM   DoLoR sit amet,,,,,,   CONSECTEUR adipiscing elit!!!!')
        print(self.review.formatted_text)
        self.assertEquals(self.review.formatted_text, 'Lorem ipsum dolor sit amet, consecteur adipiscing elit!')
