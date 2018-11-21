from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    url(
        r'^risk/$',
        views.ClientInsuranceRiskListView.as_view(),
        name='client-insurance-risks',
    ),
    url(
        r'^risk/create/$',
        # r'^risk/(?P<pk>\d+)/$',
        csrf_exempt(views.ClientInsuranceRiskCreateView.as_view()),
        name='client-insurance-risk-create',
    ),
    url(
        r'^risk/(?P<pk>\d+)/$',
        csrf_exempt(views.ClientInsuranceRiskRetrieveUpdateView.as_view()),
        name='client-insurance-risk-retrieve',
    ),
    url(
        r'^risk/(?P<pk>\d+)/edit/$',
        csrf_exempt(views.ClientInsuranceRiskRetrieveUpdateView.as_view()),
        name='client-insurance-risk-edit',
    ),
]
