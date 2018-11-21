from django.contrib import admin

from . import models


# #### INLINES #####

class ClientFieldInlineAdmin(admin.TabularInline):
    model = models.ClientField
    extra = 1

# #### INLINES #####


@admin.register(models.ClientInsuranceRisk)
class ClientInsuranceRiskAdmin(admin.ModelAdmin):
    inlines = (ClientFieldInlineAdmin,)
