from rest_framework import serializers

from . import models


class InsuranceRiskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InsuranceRisk
        fields = ('id', 'name')


class SelectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SelectOption
        fields = ('id', 'name')


class FieldSerializer(serializers.ModelSerializer):
    options = SelectOptionSerializer(many=True, required=False)
    field = serializers.IntegerField(source='id', read_only=True)   # another id field for creating ClientInsuranceRisk

    class Meta:
        model = models.Field
        fields = ('id', 'field', 'name', 'field_type', 'options')

    def validate(self, data):
        field_type = data.get('field_type')
        options = data.get('options', [])
        if field_type == models.Field.SELECT and len(options) == 0:
            raise serializers.ValidationError(
                'Cannot create enum field without options'
            )
        return data


class InsuranceRiskSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)
    insurance_risk = serializers.IntegerField(source='id', read_only=True)  # another id field for creating ClientInsuranceRisk

    class Meta:
        model = models.InsuranceRisk
        fields = ('id', 'insurance_risk', 'name', 'fields')

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        insurance_risk = models.InsuranceRisk.objects.create(**validated_data)

        for field_data in fields_data:
            options = None
            if 'options' in field_data:
                options = field_data.pop('options')

            field = models.Field.objects.create(insurance_risk=insurance_risk,
                                                **field_data)
            if options:
                for option_data in options:
                    models.SelectOption.objects.create(field=field,
                                                       **option_data)
        return insurance_risk
