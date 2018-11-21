# from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import InsuranceRisk


class InsuranceRiskListViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        for risk_num in range(10):
            InsuranceRisk.objects.create(
                name='Risk {}'.format(risk_num)
            )

    def test_fetch_insurance_risks(self):
        url = reverse('insurance-risk-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 10)


class InsuranceRiskRetrieveViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        InsuranceRisk.objects.create(id=1, name='Risk')

    def test_fetch_insurance_risk(self):
        url = reverse('insurance-risk-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Risk')


class InsuranceRiskCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        InsuranceRisk.objects.create(name='Risk duplicated')

    def setUp(self):
        self.data = {
            'name': 'New risk',
            'fields': [
                {
                    'name': 'Text field',
                    'field_type': 'text'
                },
                {
                    'name': 'Number field',
                    'field_type': 'number',
                },
                {
                    'name': 'Enum field',
                    'field_type': 'select',
                    'options': [
                        {
                            'name': 'Option 1',
                        },
                        {
                            'name': 'Option 2',
                        },
                    ],
                },
            ],
        }

    def test_create_select_field_without_options(self):
        url = reverse('insurance-risk-create')
        del self.data['fields'][2]['options']
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_select_field_with_empty_options(self):
        url = reverse('insurance-risk-create')
        self.data['fields'][2]['options'] = []
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_field_without_name(self):
        url = reverse('insurance-risk-create')
        del self.data['fields'][0]['name']
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_field_without_type(self):
        url = reverse('insurance-risk-create')
        self.data['fields'][1]['field_type'] = ''
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_risk_with_exist_name(self):
        url = reverse('insurance-risk-create')
        self.data['name'] = 'Risk duplicated'
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_risk(self):
        url = reverse('insurance-risk-create')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
