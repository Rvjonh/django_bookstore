from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

# Create your tests here.


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
    username = "newUsername"
    email = "new_user_email@example.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
