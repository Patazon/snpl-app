"""module providing for automatic functions"""

import base64
import os
from time import strftime, strptime

import requests
from django.http import JsonResponse
from django.utils import timezone
from dotenv import load_dotenv

from daraja.models import OAuthToken, TillTransaction
from daraja.serializers import TillTransactionSerializer
from dashboard.models import Payment
from dashboard.tasks import payment_sms

load_dotenv(override=True)


def basic_auth():
    """genereates the base64 encoded string for auth header"""

    auth = f"{os.getenv('PROD_CONSUMER_KEY')}:{os.getenv('PROD_CONSUMER_SECRET')}"

    byte_auth = auth.encode("utf-8")

    encoded_auth = base64.b64encode(byte_auth)

    decoded_string = encoded_auth.decode("utf-8")

    return decoded_string


def get_daraja_token():
    """consumes daraja's authorization api"""
    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    headers = {"Authorization": f"Basic {basic_auth()}"}
    # headers = {"Authorization": f"Basic {os.getenv("BASIC")}"}
    feedback = requests.get(
        url,
        headers=headers,
        timeout=35,
    ).json()

    if feedback["access_token"]:
        access_token = feedback["access_token"]
        validity = feedback["expires_in"]

        # create_token(access_token, timestamp, validity)
        tk = create_dbtoken(access_token, validity)
        return tk
    else:
        return print("Error processing API")


def create_dbtoken(tk, expire):
    """creates a new entry on the database for the token"""

    # clear database
    OAuthToken.objects.all().delete()

    # store the new token
    res = OAuthToken.objects.create(token=tk, expiry=expire)

    return res.token


def get_dbtoken():
    """gets the valid token from the database"""
    tk = OAuthToken.objects.first()
    if tk == None:
        tk = get_daraja_token()

    else:
        time_diff = timezone.now() - tk.created_at
        mins = time_diff.total_seconds() // 60
        if mins > 55:
            tk = get_daraja_token()

    return tk


def create_transdetails(till):
    """creates a new entry on the database for till transactions"""

    dbq = TillTransaction.objects.create(body=till)

    return None


def get_transdetails():
    """retrieves till transactions from the database"""

    qs = TillTransaction.objects.all()

    if qs:

        serializer = TillTransactionSerializer(qs, many=True)

        return serializer.data

    return print("No transactions")


def set_payment(msisdn, trans_id, trans_time, amount, ref_number):
    time_format = strptime(trans_time, "%Y%m%d%H%M%S")
    formatted = strftime("%d-%m-%Y %H:%M:%S", time_format)

    ref = ref_number.removeprefix("PZP")

    q = Payment.objects.filter(contract_id=ref)

    # print(q)

    Payment.objects.create(
        till_amount=int(float(amount)),
        till_trans_id=trans_id,
        till_trans_time=formatted,
        contract_id=ref,
        mode_id="m-pesa",
    )

    payment_sms(ref)
