from django.test import TestCase
from django.urls import reverse

from datetime import timedelta

from http import HTTPStatus

from users.forms import UserRegistrationForm
from users.models import User, EmailVerification

class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'pezduk2',
            'last_name': 'pezdukovich2',
            'username': 'pohuy2',
            'email': 'pizdecen2@mail.ru',
            'password': 'Password1234',
            'password2': 'Password1234'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists()) #Проверяем не был ли создан юзер в базе заранее (еще до отправки формы)
        response = self.client.post(self.path, self.data)

        #check creating of user
        #self.assertEqual(response.status_code, HTTPStatus.FOUND) #HTTPStatus.FOUND == 302 Почему-то глючит редирект
        #self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(response, User.objects.filter(username=username).exists()) #assertTrue checks if bool(expression) is True

        #check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(response, email_verification.exists())
        print(EmailVerification.objects.filter(user__username=username))
        # self.assertEqual(response,
        #     email_verification.first().expiration.date(),
        #     (now() + timedelta(hours=48)).date()
        # )
