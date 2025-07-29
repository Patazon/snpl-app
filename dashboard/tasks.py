import os

import requests
from django.db.models import Sum

from dashboard.models import Client, Contract, Payment


def reminder_sms():
    pending = list(
        Contract.objects.filter(status__standing__icontains="pending").values_list(
            "client_id", flat=True
        )
    )

    msisdns = list(
        Client.objects.filter(id_number__in=pending).values_list("msisdn", flat=True)
    )

    # print(pending)
    # print(msisdns)

    url = "https://api.tililtech.com/sms/v3/sendsms"

    headers = {"Content-Type": "application/json"}

    for msisdn in msisdns:
        payload = {
            "api_key": os.getenv("TILIL_KEY"),
            "service_id": 0,
            "mobile": msisdn,
            "response_type": "json",
            "shortcode": "Patazone",
            "message": f"Dear Customer, kindly remember to complete your PatazonePay payments. Have a good day. Call 0111051120 for more products or visit https://www.patazone.co.ke",
        }

        feedback = requests.post(url, headers=headers, json=payload, timeout=20).json()

    pass


def new_contract_sms(client):

    client_details = Client.objects.get(id_number=client)

    contract_details = Contract.objects.filter(client_id=client).latest("created_at")

    # print(client_details.msisdn)

    url = "https://api.tililtech.com/sms/v3/sendsms"

    headers = {"Content-Type": "application/json"}

    payload = {
        "api_key": os.getenv("TILIL_KEY"),
        "service_id": 0,
        "mobile": f"254{client_details.msisdn}",
        "response_type": "json",
        "shortcode": "Patazone",
        "message": f"Dear {client_details.name}, thank you for opening a SNPL contract for {contract_details.product} at KES {contract_details.price}. For inquiries call 0111051120",
    }
    feedback = requests.post(url, headers=headers, json=payload, timeout=20).json()

    return feedback


def payment_sms(contract):

    bank = Payment.objects.filter(contract_id=contract).aggregate(
        Sum("bank_amount", default=0)
    )
    till = Payment.objects.filter(contract_id=contract).aggregate(
        Sum("till_amount", default=0)
    )
    cash = Payment.objects.filter(contract_id=contract).aggregate(
        Sum("cash_amount", default=0)
    )

    # print(bank,till, cash)
    sum = bank["bank_amount__sum"] + till["till_amount__sum"] + cash["cash_amount__sum"]
    print(sum)

    contract_details = Contract.objects.filter(id=contract).values_list(
        "client", "price"
    )[0]

    # print(contract_details)

    client_details = Client.objects.get(id_number=contract_details[0])

    # print(client_details.msisdn)

    balance = contract_details[1] - sum

    url = "https://api.tililtech.com/sms/v3/sendsms"

    headers = {"Content-Type": "application/json"}

    payload = {
        "api_key": os.getenv("TILIL_KEY"),
        "service_id": 0,
        "mobile": f"254{client_details.msisdn}",
        "response_type": "json",
        "shortcode": "Patazone",
        "message": f"Dear Customer, you have paid a total of KES {sum}. Your balance is KES {balance}. For more inquiries call 0111051120",
    }
    feedback = requests.post(url, headers=headers, json=payload, timeout=20).json()

    return feedback
