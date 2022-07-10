from django.test import TestCase
from django.urls import reverse

from . import services


class ServicesTestCase(TestCase):
    """Test services"""

    def test_get_currencies_values(self):
        result = services.get_currencies_values()
        self.assertIsInstance(result, dict)

    def test_successful_convert_1(self):
        amount = 1
        primary_currency = 'USD'
        secondary_currency = 'RUB'
        currencies = {
            'USD': 1.00,
            'RUB': 25.00,
        }

        result = services.convert(amount, primary_currency, secondary_currency, currencies)

        self.assertEqual(result, 25.00)

    def test_successful_convert_2(self):
        amount = 1
        primary_currency = 'EUR'
        secondary_currency = 'RUB'
        currencies = {
            'USD': 1.00,
            'EUR': 0.959,
            'RUB': 25.00,
        }

        result = services.convert(amount, primary_currency, secondary_currency, currencies)

        self.assertEqual(result, 26.07)

    def test_unsuccessful_convert(self):
        amount = 1
        primary_currency = 'EUR'
        secondary_currency = 'RUB'
        currencies = {
            'USD': 1.00,
            'EUR': 0,
            'RUB': 25.00,
        }
        with self.assertRaises(services.exceptions.ExchangeRateException):
            result = services.convert(amount, primary_currency, secondary_currency, currencies)


class ConvertViewTestCase(TestCase):
    """Test 'convert' view"""

    def test_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'converter/index.html')

    def test_post_with_correct_form(self):
        data = {
            'amount': '1',
            'primary_currency': 'USD',
            'secondary_currency': 'RUB',
        }
        response = self.client.post(reverse('home'), data=data)
        self.assertEqual(response.status_code, 200)
        converted_amount = response.context['converted_amount']
        self.assertIsInstance(converted_amount, float)
        self.assertTrue(converted_amount >= 0)
