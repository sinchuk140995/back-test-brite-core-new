from rest_framework import generics

from . import models
from . import serializers


class InsuranceRiskListView(generics.ListAPIView):
    queryset = models.InsuranceRisk.objects.all()
    serializer_class = serializers.InsuranceRiskListSerializer


class InsuranceRiskCreateView(generics.CreateAPIView):
    queryset = models.InsuranceRisk.objects.all()
    serializer_class = serializers.InsuranceRiskSerializer


class InsuranceRiskRetrieveView(generics.RetrieveAPIView):
    serializer_class = serializers.InsuranceRiskSerializer
    queryset = models.InsuranceRisk.objects.all()


# class TestInsuranceRiskRetrieve(APIView):

#     def get(self, request, format=None, *args, **kwargs):
#         try:
#             insurance_risk = models.InsuranceRisk.objects.get(pk=kwargs['pk'])
#         except models.InsuranceRisk.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         risk_fields = []
#         for field in insurance_risk.fields.all():
#             field_data = {
#                 'field': field.pk,
#                 'name': field.name,
#                 'field_type': field.field_type,
#             }

#             if field.field_type == models.Field.SELECT:
#                 options = []
#                 for option in field.options.all():
#                     options.append({
#                         'id': option.id,
#                         'name': option.name,
#                     })
#                 field_data['options'] = options

#             risk_fields.append(field_data)

#         insurance_data = {
#             'insurance_risk': insurance_risk.id,
#             'name': insurance_risk.name,
#             'client_fields': risk_fields,
#         }

#         return Response(insurance_data)
