from django.test import TestCase
from accounts.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import get_user_model
from model_bakery import baker

User = get_user_model()



class TestRegistrationForm(TestCase):
    form = UserRegistrationForm

    @classmethod
    def setUpTestData(cls):
        baker.make(User, email='a@a.com')
        baker.make(User, phone_number='0987654321')

    def test_valid_form(self):
        form = self.form(
            data={
                'phone_number':'0917654321',
                'email':'a@1a.com',
                'first_name':'a',
                'last_name':'b',
                'password':'123123',
                'verification_method':'email',
            }
        )
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = self.form(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),6)
    
    def test_email_phone_number_exists(self):
        form = self.form(
            data={
                'phone_number':'0987654311',
                'email':'a@a.com',
                'first_name':'a',
                'last_name':'b',
                'password':'123123',
                'verification_method':'email',
            }
        )
        self.assertFalse(form.is_valid(), 'email verification for existing user failed!!')
        self.assertEqual(len(form.errors),1)
        form = self.form(
            data={
                'phone_number':'0987654321',
                'email':'a@aa.com',
                'first_name':'a',
                'last_name':'b',
                'password':'123123',
                'verification_method':'email',
            }
        )
        self.assertFalse(form.is_valid(), 'phone_number verification for existing user failed!!')
        self.assertEqual(len(form.errors),1)


class TestLoginForm(TestCase):
    form = UserLoginForm
    
    @classmethod
    def setUpTestData(cls):
        baker.make(User, phone_number="0987654321")

    def test_user_exists(self):
        form = self.form(
            data={
                'phone_number':'0987654320',
                'password':'123123',
            }
        )
        self.assertFalse(form.is_valid(), 'there is error on phone number check from db!!')
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('phone_number'))
    
    def test_user_active(self):
        form = self.form(
            data={
                'phone_number':'0987654321',
                'password':'123123',
            }
        )
        self.assertFalse(form.is_valid(), 'there is error on is active check for user!!')
        self.assertEqual(len(form.errors), 1)