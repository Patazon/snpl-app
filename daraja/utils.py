"""module providing for automatic functions"""

import base64
import os
from time import strftime, strptime

import requests
from django.http import JsonResponse
from django.utils import timezone
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from rest_framework import response, status

from daraja.models import CallbackResults, OAuthToken, TillTransaction, Transaction
from daraja.serializers import CallbackResultsSerializer, TillTransactionSerializer
from dashboard.models import Payment
from dashboard.tasks import payment_sms

load_dotenv(override=True)


def basic_auth():
    """genereates the base64 encoded string for auth header"""

    auth = f"{os.getenv('CONSUMER_KEY')}:{os.getenv('CONSUMER_SECRET')}"

    byte_auth = auth.encode("utf-8")

    encoded_auth = base64.b64encode(byte_auth)

    decoded_string = encoded_auth.decode("utf-8")

    return decoded_string


def basic_password():
    timestamp = strftime("%Y%m%d%H%M%S")

    password = f"{os.getenv('EXPRESS_SHORT_CODE')}{os.getenv('PASSKEY')}{timestamp}"

    byte_password = password.encode("utf-8")

    encoded_password = base64.b64encode(byte_password)

    decoded_pass = encoded_password.decode("utf-8")

    return decoded_pass


def get_daraja_token():
    """consumes daraja's authorization api"""
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

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

    ref = ref_number.removeprefix("PZP-000")

    q = Payment.objects.filter(contract_id=ref)

    print(q)

    Payment.objects.create(
        till_amount=int(float(amount)),
        till_trans_id=trans_id,
        till_trans_time=formatted,
        contract_id=ref,
        mode_id="m-pesa",
    )

    # payment_sms(ref)


def log_callback(resp):
    # contract = log_contract(contract)
    if resp:
        log = CallbackResults.objects.create(body=resp)

        body = log.body

        if body["Body"]["stkCallback"]["ResultCode"] == 0:
            filt_body = Payment.objects.create(
                till_amount=body["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0][
                    "Value"
                ],
                till_trans_id=body["Body"]["stkCallback"]["CallbackMetadata"]["Item"][
                    1
                ]["Value"],
                till_trans_time=body["Body"]["stkCallback"]["CallbackMetadata"]["Item"][
                    3
                ]["Value"],
                mode_id="m-pesa",
            )

            return filt_body
        return None


def get_callback():
    logs = CallbackResults.objects.all()
    serializer = CallbackResultsSerializer(logs, many=True)

    return serializer
