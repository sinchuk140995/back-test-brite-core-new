from django.db import models
from django.utils.translation import gettext_lazy as _


class InsuranceRisk(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    post_date = models.DateTimeField(_('post date'), auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Field(models.Model):
    STRING = 'text'
    NUMBER = 'number'
    SELECT = 'select'
    TYPE_CHOICES = (
        (STRING, 'String'),
        (NUMBER, 'Number'),
        (SELECT, 'Enum'),
    )

    name = models.CharField(_('name'), max_length=50)
    insurance_risk = models.ForeignKey(
        InsuranceRisk,
        verbose_name=_('insurance risk'),
        related_name='fields',
    )
    # field_type = models.PositiveSmallIntegerField(_('type'), choices=TYPE_CHOICES)
    field_type = models.CharField(_('type'), max_length=10, choices=TYPE_CHOICES)

    # class Meta:
    #     ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def is_select(self):
        return self.field_type == self.SELECT


class SelectOption(models.Model):
    name = models.CharField(_('name'), max_length=50)
    field = models.ForeignKey(
        Field,
        verbose_name=_('select field'),
        related_name='options',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
