from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from . import factories

User = get_user_model()
from reviews.models import Doctor, ExceptionWord, Fword


class TestReviewPages(TestCase):
    def setUp(self):
        self.regular_сlient = Client()
        self.staff_client = Client()
        self.staff_user = factories.UserFactory(username='staff_test', is_staff=True)
        self.regular_user = factories.UserFactory(username='test')
        self.fword = Fword.objects.create(word="БЛять")
        self.exception_word = ExceptionWord.objects.create(word="оскорблять")
        self.doctor = factories.DoctorFactory(first_name="Ай", last_name="Болит", patronymic="Вениаминович")
        self.specialty = self.doctor.spec.create(title="Therapist")

    def test_review_list_page(self):
        self.staff_client.force_login(self.staff_user)
        self.assertEqual(self.staff_client.get("/reviews/").status_code, 200)

    def test_review_list_unauthorized(self):
        self.assertRedirects(
            self.regular_сlient.get("/reviews/"),
            "/admin/login/?next=/reviews/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_new_review_format(self):
        self.staff_client.force_login(self.staff_user)
        self.staff_client.post(
            f"/add-review/{self.doctor.id}/",
            {
                "text": """   LOREM  IPSUM УУУБЛЯТЬ!!!!!!  Dolor, ОсКоРбЛяТь. sit
                amet consectetur adipiscing elit. Donec vehicula eros at leo ullamcorper accumsan.
                Quisque facilisis, metus quis pretium commodo, nunc tellus
                consequat dui, quis posuere mauris odio sed dui. Donec non massa
                dictum, varius est id, condimentum magna. Vestibulum varius,    metus ut blandit euismod, magna arcu malesuada
                velit, a tristique eros dui ut tortor. Nullam turpis massa, efficitur
                nec pretium in, ultricies eu ante. Donec non elementum magna, scelerisque
                suscipit nulla. Aenean id vehicula ante, ac convallis ante. Aenean sed
                tempor arcu. Integer porta, ipsum sed semper elementum, erat turpis
                tempus lacus, ut ultricies sapien ipsum eu turpis. Sed.  """
            },
        )
        response = self.staff_client.get("/reviews/")
        self.assertContains(response, "Автор: staff_test")
        self.assertContains(response, "Врач: Болит Ай Вениаминович")
        self.assertContains(response, "Специальность: Therapist")
        self.assertContains(
            response,
            'Lorem ipsum <span style="color: red;">ууублять!</span> Dolor, оскорблять. Sit amet consectetur',
        )
