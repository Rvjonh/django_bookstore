from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

# Create your tests here.

from .forms import CustomUserCreationForm
from .views import SignupPageView


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        normal_user = User.objects.create_user(
            username="fernando",
            email="fer_gonzoales27@gmail.com",
            password="gonza456fer",
        )
        self.assertEqual(normal_user.username, "fernando")
        self.assertEqual(normal_user.email, "fer_gonzoales27@gmail.com")
        self.assertTrue(normal_user.is_active)
        self.assertFalse(normal_user.is_staff)
        self.assertFalse(normal_user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        normal_user = User.objects.create_superuser(
            username="CR7",
            email="ronaldoCR7@portugal.com",
            password="super-bicho",
        )
        self.assertEqual(normal_user.username, "CR7")
        self.assertEqual(normal_user.email, "ronaldoCR7@portugal.com")
        self.assertTrue(normal_user.is_active)
        self.assertTrue(normal_user.is_staff)
        self.assertTrue(normal_user.is_superuser)


class SignUpPageTest(TestCase):
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "registration/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_signup_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_signup_view(self):
        view = resolve("/accounts/signup/")
        self.assertEqual(view.func.__name__, SignupPageView.as_view().__name__)
