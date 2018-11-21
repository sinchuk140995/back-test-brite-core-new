from django.db import models
from django.utils.translation import ugettext_lazy as _

from risks import models as risk_models


class ClientInsuranceRisk(models.Model):
    insurance_risk = models.ForeignKey(
        risk_models.InsuranceRisk,
        verbose_name=_('insurance risk'),
        related_name='client_risks',
    )
    post_date = models.DateTimeField(_('post date'), auto_now_add=True)

    class Meta:
        ordering = ('-post_date',)

    def __str__(self):
        return self.insurance_risk.name


class ClientField(models.Model):
    client_insurance_risk = models.ForeignKey(
        ClientInsuranceRisk,
        verbose_name=_('client insurance risk'),
        related_name='fields',
    )
    field = models.ForeignKey(
        risk_models.Field,
        verbose_name=_('field'),
        related_name='client_fields',
    )
    value = models.CharField(
        _('value'),
        max_length=255,
        blank=True,
    )
    select_option = models.ForeignKey(
        risk_models.SelectOption,
        verbose_name=_('selected option'),
        related_name='options',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('field',)
