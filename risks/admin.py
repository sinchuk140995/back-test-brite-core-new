from django.contrib import admin

from . import models


# #### INLINES #####

class FieldInlineAdmin(admin.TabularInline):
    model = models.Field
    extra = 1

# #### INLINES #####


@admin.register(models.InsuranceRisk)
class InsuranceRiskAdmin(admin.ModelAdmin):
    inlines = (FieldInlineAdmin,)


@admin.register(models.SelectOption)
class SelectOptionAdmin(admin.ModelAdmin):
    pass
