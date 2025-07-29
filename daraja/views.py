"""module providing for views"""

import json
import os
from time import strftime

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv
from rest_framework import response, status
from rest_framework.views import APIView, View

from daraja.utils import (
    basic_password,
    create_transdetails,
    get_callback,
    get_dbtoken,
    get_transdetails,
    log_callback,
    set_payment,
)

load_dotenv(override=True)


class Webhook(View):
    """single cbv to display data"""

    def get(self, request):
        """loads all recent till transactions"""

        tr = get_transdetails()
        if tr:
            return render(request, "daraja/daraja.html", {"res": tr})
        return render(request, "daraja/daraja.html")

    def post(self, request):
        """webhook listens for new transactions"""

        resp = json.loads(request.body)

        create_transdetails(resp)

        # print(resp)

        msisdn = str({None: ""}.get(resp["MSISDN"], resp["MSISDN"]))
        trans_id = str({None: ""}.get(resp["TransID"], resp["TransID"]))
        trans_time = str({None: ""}.get(resp["TransTime"], resp["TransTime"]))
        amount = str({None: ""}.get(resp["TransAmount"], resp["TransAmount"]))
        ref_number = str(
            {None: ""}.get(resp["BillRefNumber"], resp["BillRefNumber"])
        )  # noqa

        set_payment(msisdn, trans_id, trans_time, amount, ref_number)

        return render(request, "daraja/daraja.html", {"resp": resp})


def register_urls(request):
    """registers urls for validation and confirmation"""
    tk = get_dbtoken()

    url = "https://api.safaricom.co.ke/mpesa/c2b/v2/registerurl"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tk}",
    }
    print(headers)

    payload = {
        "ShortCode": os.getenv("PROD_SHORT_CODE"),
        "ResponseType": "Completed",
        "ConfirmationURL": os.getenv("CONFIRMATION_URL"),
        "ValidationURL": os.getenv("VALIDATION_URL"),
    }

    # print(payload)

    feedback = requests.post(
        url, headers=headers, json=payload, timeout=30
    ).json()  # noqa

    return JsonResponse(feedback)
