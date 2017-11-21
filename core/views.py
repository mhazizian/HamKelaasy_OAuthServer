# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView


# Create your views here.
def my_login(request):
    return HttpResponse('salam')


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2! Get')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2! Post')
