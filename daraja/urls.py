from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from daraja.views import Webhook, register_urls

urlpatterns = [
    path("confirmation/", csrf_exempt(Webhook.as_view())),
    path("urls/", register_urls, name="register_urls"),
]
