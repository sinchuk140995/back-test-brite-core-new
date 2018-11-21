from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    url(
        r'^risk/$',
        views.InsuranceRiskListView.as_view(),
        name='insurance-risk-list',
    ),

    url(
        r'^risk/create/$',
        views.InsuranceRiskCreateView.as_view(),
        name='insurance-risk-create',
    ),

    url(
        r'^risk/(?P<pk>\d+)/$',
        views.InsuranceRiskRetrieveView.as_view(),
        name='insurance-risk-detail',
    ),

]
