from django.test import TestCase
from django.urls import reverse

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
