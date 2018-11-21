"""back_test_brite_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from risks import views


urlpatterns = [
    url(r'^api/client/', include('clients.urls')),
    url(r'^api/', include('risks.urls')),

    # url(r'^api/risk/create/$', csrf_exempt(views.InsuranceRiskCreateView.as_view()), name='insurance-risk-create'),
    # url(r'^api/client/risk/$', views.ClientInsuranceRiskListView.as_view(), name='client-insurance-risks'),
    # url(r'^api/client/risk/(?P<pk>\d+)/$', csrf_exempt(views.InsuranceRiskTakeView.as_view()), name='insurance-risk-take'),
    # url(r'^api/client/risk/(?P<pk>\d+)/edit/$', csrf_exempt(views.InsuranceRiskEditView.as_view()), name='insurance-risk-edit'),
    url(r'^admin/', admin.site.urls),
]
