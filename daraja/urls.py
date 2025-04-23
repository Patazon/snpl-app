from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from daraja.views import STKCallback, STKexpress, Webhook, register_urls

urlpatterns = [
    path("confirmation/", csrf_exempt(Webhook.as_view())),
    path("urls/", register_urls, name="register_urls"),
    path("stkpush/", STKexpress, name="stkpush"),
    path("callback/", csrf_exempt(STKCallback.as_view()), name="callback"),
]
