from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.forms import UserRegistrationForm
from django.urls import reverse

User = get_user_model()


class TestUserRegistrationView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = Client
    
    def test_get_method(self):
        response = self.client.get(path=reverse('accounts:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertIsInstance(response.context['form'], UserRegistrationForm)
    
    def test_post_method_valid(self):
        response = self.client.post(reverse('accounts:user_register'), data={
                'phone_number':'0917654321',
                'email':'a@1a.com',
                'first_name':'a',
                'last_name':'b',
                'password':'123123',
                'verification_method':'email',})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
    
    def test_post_method_invalid(self):
        response = self.client.post(reverse('accounts:user_register'), data={
                'phone_number':'0917654321',
                'email':'a',
                'first_name':'a',
                'last_name':'b',
                'password':'123123',
                'verification_method':'email',})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', errors='Enter a valid email address.')