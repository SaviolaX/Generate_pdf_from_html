from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .forms import SignUpForm
from .views import SignUpView


class BaseTest(TestCase):
    
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123'
        )
        self.user_auth = {
            'username': 'will',
            'password': 'testpass123'}
        


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignupPageTests(BaseTest):

    def test_signup_template(self):
        self.response = self.client.get(self.signup_url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/register.html')
        self.assertContains(self.response, 'Register')
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')
    
    def test_signup_form(self):
        self.response = self.client.get(self.signup_url)
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class LoginPageTests(BaseTest):

    def test_can_access_page(self):
        self.response = self.client.get(self.login_url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/login.html')
        self.assertContains(self.response, 'Login')
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')


class LogOutPageTests(BaseTest):

    def test_logout_url_name_code(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)