# from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from risks import models as risks_models
from .models import ClientInsuranceRisk


class ClientInsuranceRiskListViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        for risk_num in range(10):
            insurance_risk = risks_models.InsuranceRisk.objects.create(
                name='Risk {}'.format(risk_num)
            )
            ClientInsuranceRisk.objects.create(
                insurance_risk=insurance_risk
            )

    def test_fetch_client_insurance_risks(self):
        url = reverse('insurance-risk-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 10)


class ClientInsuranceRiskRetrieveUpdateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        insurance_risk = risks_models.InsuranceRisk.objects.create(
            name='Risk'
        )
        ClientInsuranceRisk.objects.create(
            id=1,
            insurance_risk=insurance_risk,
        )

    def test_fetch_client_insurance_risk(self):
        url = reverse('client-insurance-risk-retrieve', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Risk')


class ClientInsuranceRiskCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        insurance_risk = risks_models.InsuranceRisk.objects.create(
            id=1,
            name='Risk',
        )
        field_types = (
            risks_models.Field.STRING,
            risks_models.Field.NUMBER,
            risks_models.Field.SELECT,
        )
        for idx, field_type in enumerate(field_types):
            risks_models.Field.objects.create(
                id=idx,
                insurance_risk=insurance_risk,
                name='Field {}'.format(idx),
                field_type=field_type,
            )

        select_field = risks_models.Field.objects \
            .get(field_type=risks_models.Field.SELECT)

        for option_id in range(3):
            risks_models.SelectOption.objects.create(
                id=option_id,
                name='Option {}'.format(option_id),
                field=select_field,
            )

    def setUp(self):
        insurance_risk = risks_models.InsuranceRisk.objects.get(id=1)
        self.data = {
            'insurance_risk': insurance_risk.id,
        }

        fields = list()
        for field in insurance_risk.fields.all():
            field_data = {
                'field': field.id
            }
            if field.field_type == risks_models.Field.STRING:
                field_data['value'] = 'Text'
            elif field.field_type == risks_models.Field.NUMBER:
                field_data['value'] = 123
            elif field.field_type == risks_models.Field.SELECT:
                field_data['select_option'] = field.options.first().id

            fields.append(field_data)
        self.data['fields'] = fields

    def test_create_client_risk_with_empty_text_value(self):
        url = reverse('client-insurance-risk-create')
        self.data['fields'][0]['value'] = ''
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_client_risk_without_number_value(self):
        url = reverse('client-insurance-risk-create')
        del self.data['fields'][1]['value']
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_client_risk_with_empty_select_options(self):
        url = reverse('client-insurance-risk-create')
        self.data['fields'][2]['select_option'] = ''
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_client_risk(self):
        url = reverse('client-insurance-risk-create')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
