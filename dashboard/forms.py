from django import forms
from django.db import models
from django.forms import ModelForm

from dashboard.models import Client, Contract, Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["item", "model"]
        labels = {
            "item": "",
            "model": "",
        }
        widgets = {
            "item": forms.TextInput(
                attrs={"placeholder": "Nunix Free Standing Oven Cooker KZ-560-3G1E"}
            ),
            "model": forms.TextInput(attrs={"placeholder": "MKD-16846464"}),
        }


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = [
            "client",
            "price",
            "product",
            "expiry",
            "status",
            "branch",
            "salesrep",
        ]
        labels = {
            "client": "",
            "price": "",
            "product": "",
            "expiry": "",
            "status": "",
            "branch": "",
            "salesrep": "",
        }
        widgets = {
            "client": forms.Select(attrs={"placeholder": "Client Name"}),
            "price": forms.NumberInput(attrs={"placeholder": "Price"}),
            "product": forms.Select(),
            "expiry": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "status": forms.Select(attrs={"value": "pending"}),
            "branch": forms.Select(attrs={"value": "RNG Plaza"}),
            "salesrep": forms.Select(attrs={"placeholder": "sales representative"}),
        }


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ["id_number", "name", "msisdn"]
        labels = {
            "id_number": "",
            "name": "",
            "msisdn": "",
        }
        widgets = {
            "id_number": forms.NumberInput(attrs={"placeholder": "ID number"}),
            "name": forms.TextInput(attrs={"placeholder": "James Bond"}),
            "msisdn": forms.TextInput(attrs={"placeholder": "700123456"}),
        }


class UpdateContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ["client", "price", "product", "expiry", "status", "salesrep"]
        labels = {
            "client": "",
            "price": "",
            "product": "",
            "expiry": "",
            "status": "",
            "salesrep": "",
        }
        widgets = {
            "client": forms.Select(),
            "price": forms.NumberInput(),
            "product": forms.Select(),
            "expiry": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "status": forms.Select(),
            "salesrep": forms.Select(),
        }


class RedeemProductForm(ModelForm):
    class Meta:
        model = Contract
        fields = ["client", "price", "product", "expiry", "status", "salesrep"]
        labels = {
            "client": "",
            "price": "",
            "product": "",
            "expiry": "",
            "status": "",
            "salesrep": "",
        }
        widgets = {
            "product": forms.Select(),
        }
