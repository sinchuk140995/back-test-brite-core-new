from rest_framework import serializers

from . import models
from risks.models import SelectOption
from risks.serializers import SelectOptionSerializer


class ClientInsuranceRiskListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='insurance_risk.name', read_only=True)

    class Meta:
        model = models.ClientInsuranceRisk
        fields = ('id', 'name', 'post_date')


class ClientFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)   # for accessing id in nested serializer
    name = serializers.CharField(source='field.name', read_only=True)
    field_type = serializers.CharField(source='field.field_type', read_only=True)
    options = serializers.SerializerMethodField()

    class Meta:
        model = models.ClientField
        fields = ('id', 'field', 'value', 'name',
                  'select_option', 'field_type', 'options')

    def get_options(self, obj):
        if obj.select_option:
            select_options = SelectOption.objects.filter(field=obj.select_option.field)
            return SelectOptionSerializer(select_options, many=True).data

    def validate(self, data):
        if data.get('value') and data.get('select_option'):
            raise serializers.ValidationError('You cannot choose value and option')
        elif not (data.get('value') or data.get('select_option')):
            raise serializers.ValidationError('Choose value or option')
        return data


class ClientFieldCreateSerializer(ClientFieldSerializer):
    class Meta:
        model = models.ClientField
        fields = ('field', 'value', 'name',
                  'select_option', 'field_type', 'options')


class ClientInsuranceRiskSerializer(serializers.ModelSerializer):
    fields = ClientFieldSerializer(many=True)
    name = serializers.CharField(source='insurance_risk.name', read_only=True)

    class Meta:
        model = models.ClientInsuranceRisk
        fields = ('id', 'insurance_risk', 'name',
                  'post_date', 'fields')

    def create(self, validated_data):
        fields = validated_data.pop('fields')
        client_insurance_risk = models.ClientInsuranceRisk.objects \
            .create(**validated_data)

        for field_data in fields:
            models.ClientField.objects.create(
                client_insurance_risk=client_insurance_risk,
                **field_data
            )
        return client_insurance_risk

    def update(self, instance, validated_data):
        # instance.insurance_risk = validated_data.get('insurance_risk', instance.insurance_risk)
        # instance.save()

        fields = validated_data.get('fields')

        for field_data in fields:
            field_id = field_data.get('id', None)

            if not field_id:
                continue

            client_field = models.ClientField.objects.get(id=field_id, client_insurance_risk=instance)
            if client_field.field.is_select:
                client_field.select_option = field_data.get('select_option', client_field.select_option)
            else:
                client_field.value = field_data.get('value', client_field.value)
            client_field.save()

        return instance


class ClientInsuranceRiskCreateSerializer(ClientInsuranceRiskSerializer):
    fields = ClientFieldCreateSerializer(many=True)
