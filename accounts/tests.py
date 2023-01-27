from django.contrib.auth import get_user_model
from django.test import TestCase

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
