"""accountant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
import rest_framework.urls

import core.urls
import interface.urls
import ng.urls

urlpatterns = (
    url(r'^ui/', include(interface.urls, namespace='ui')),
    url(r'^api/', include(core.urls)),
    url(r'^api-auth/', include(rest_framework.urls,
        namespace='rest_framework')),
    url(r'^', include(ng.urls, namespace='ng')),
)
