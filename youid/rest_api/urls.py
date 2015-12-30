from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url

urlpatterns = [
    url(r'^api-token-auth/', obtain_auth_token)
]
