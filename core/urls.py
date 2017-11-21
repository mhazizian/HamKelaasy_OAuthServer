from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^login$', views.my_login, name='login'),
    url(r'^salam$', views.ApiEndpoint.as_view()),
]
