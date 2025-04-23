import csv
from datetime import date, datetime, timedelta
from time import strftime, strptime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render

from dashboard.forms import (
    ClientForm,
    ContractForm,
    ProductForm,
    RedeemProductForm,
    UpdateContractForm,
)
from dashboard.models import Branch, Client, Contract, Payment, Product, Salesteam
from dashboard.tasks import new_contract_sms, payment_sms


# Create your views here.
@login_required(login_url="login")
def Index(request):
    """default page"""

    snpl_contracts = Contract.objects.all()[:7]

    total_products = Product.objects.count()

    total_bank = Payment.objects.aggregate(Sum("bank_amount", default=0))
    total_till = Payment.objects.aggregate(Sum("till_amount", default=0))
    total_cash = Payment.objects.aggregate(Sum("cash_amount", default=0))

    sums = (
        total_bank["bank_amount__sum"]
        + total_till["till_amount__sum"]
        + total_cash["cash_amount__sum"]
    )

    total_contracts = Contract.objects.aggregate(Sum("price")).get("price__sum")  # noqa

    print(total_contracts)

    arrears = total_contracts - sums

    pending = (
        Contract.objects.filter(status__standing__icontains="pending")
        .aggregate(Count("status"))
        .get("status__count")
    )  # noqa
    completed = (
        Contract.objects.filter(status__standing__contains="completed")
        .aggregate(Count("status"))
        .get("status__count")
    )

    redeemed = (
        Contract.objects.filter(status__standing__contains="redeemed")
        .aggregate(Count("status"))
        .get("status__count")
    )

    closed = completed + redeemed

    return render(
        request,
        "dashboard/index.html",
        {
            "contracts": snpl_contracts,
            "products": total_products,
            "bank": total_bank,
            "till": total_till,
            "cash": total_cash,
            "paid": sums,
            "arrears": arrears,
            "pending": pending,
            "completed": closed,
        },
    )


@login_required(login_url="login")
def contract(request):
    """view for contracts"""

    # order_by to prevent 'Pagination may yield inconsistent results with an
    # unordered object_list' error

    contract_list = Contract.objects.order_by("-id")

    pgs = Paginator(contract_list, 7)

    # "page" is a paginator value not assigned

    page_number = request.GET.get("page")

    content_list = pgs.get_page(page_number)

    return render(
        request,
        "dashboard/contract.html",
        {"content_list": content_list},
    )


@login_required(login_url="login")
def client(request):
    """view for clients"""
    # the hyphen is to arrange in descending order
    parties = Client.objects.order_by("-id")

    pgs = Paginator(parties, 7)

    page_number = request.GET.get("page")

    content_list = pgs.get_page(page_number)

    context = {"content_list": content_list}

    return render(request, "dashboard/client.html", context=context)


@login_required(login_url="login")
def product(request):
    """view for products"""

    products = Product.objects.order_by("-id")

    pgs = Paginator(products, 9)

    page_number = request.GET.get("page")

    content_list = pgs.get_page(page_number)

    context = {"content_list": content_list}

    return render(request, "dashboard/product.html", context=context)


@login_required(login_url="login")
def payment(request):
    """views for payment made and options"""

    payments = Payment.objects.order_by("-id")

    contracts = Contract.objects.order_by("-id")

    pgs = Paginator(payments, 12)

    page_number = request.GET.get("page")

    content_list = pgs.get_page(page_number)

    context = {"content_list": content_list, "contracts": contracts}

    return render(request, "dashboard/payment.html", context=context)


@login_required(login_url="login")
def search(request):
    """view for search result"""

    if request.method == "GET":

        searched = request.GET["searched"]

        clients = Client.objects.filter(name__icontains=searched)

        # print(clients)

        if clients:

            return render(
                request, "dashboard/search-result.html", {"clients": clients}
            )  # noqa

        return render(request, "dashboard/not-found.html")

    return render(request, "dashboard/index.html", {})


@login_required(login_url="login")
def show_search(request, searched_id):
    """view for all data pertaining to client based on search"""

    sr_party = Client.objects.get(pk=searched_id)

    # print(sr_party.id)

    sr_contracts = (
        Contract.objects.filter(client_id=sr_party.id_number)
        .values(
            "id",
            "price",
            "client_id",
            "status_id",
            "product_id",
            "branch_id",
            "salesrep_id",
            "expiry",
            "created_at",
        )
        .order_by("-id")
    )
    # print(sr_contracts)
    if sr_contracts.exists():
        sr_pending = list(
            filter(lambda x: x["status_id"] == "pending", sr_contracts)
        )  # noqa
        # print(sr_contracts)
        # print(sr_pending)
        total = sr_contracts[0]["price"]
        # print(total)
        # total = [sr_contracts[i]["price"] for i in (0, -1)]

        sr_payments = (
            Payment.objects.filter(contract_id=sr_contracts[0]["id"])
            .values(
                "id",
                "cash_amount",
                "cash_date_paid",
                "till_trans_id",
                "till_amount",
                "till_trans_time",
                "bank_ref_id",
                "bank_amount",
                "bank_transfer_time",
                "bank_account_name",
                "mode",
                "contract",
                "created_at",
            )
            .order_by("-id")
        )
        # print(sr_payments)
        sr_till = (
            Payment.objects.filter(contract_id=sr_contracts[0]["id"])
            .aggregate(Sum("till_amount", default=0))
            .get("till_amount__sum")
        )

        sr_bank = (
            Payment.objects.filter(contract_id=sr_contracts[0]["id"])
            .aggregate(Sum("bank_amount", default=0))
            .get("bank_amount__sum")
        )

        sr_cash = (
            Payment.objects.filter(contract_id=sr_contracts[0]["id"])
            .aggregate(Sum("cash_amount", default=0))
            .get("cash_amount__sum")
        )

        sr_paid = sr_cash + sr_bank + sr_till

        # print(sr_till, sr_bank, sr_cash)
        # print(sr_paid)
        # print(sr_payments)
        pages = Paginator(sr_contracts, 2)
        page_number = request.GET.get("paging")
        contract_list = pages.get_page(page_number)

        pgs = Paginator(sr_payments, 4)
        pg_no = request.GET.get("page")
        payment_list = pgs.get_page(pg_no)

        return render(
            request,
            "dashboard/search-detail.html",
            {
                "party": sr_party,
                "item_list": contract_list,
                "content_list": payment_list,
                "paid": sr_paid,
                "total": total,
            },
        )

    return render(request, "dashboard/not-found.html")


def add_client(request):
    """view for creating a client"""
    clients = Client.objects.all().order_by("-id")

    pgs = Paginator(clients, 6)
    pg_num = request.GET.get("page")
    client_list = pgs.get_page(pg_num)

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("client")

    return render(
        request,
        "dashboard/add-client.html",
        {"form": ClientForm, "content_list": client_list},
    )
    # if request.method == "GET":
    #     id = request.GET["id_number"]
    #     name = request.GET["name"]
    #     msisdn = request.GET["msisdn"]
    #     alt_msisdn = request.GET["alt-msisdn"]

    #     # print(id, name, msisdn, alt_msisdn)

    #     Client.objects.create(
    #         id_number=id, name=name, msisdn=msisdn, alt_msisdn=alt_msisdn
    #     )

    #     return redirect("client")


def update_client(request, client_id):
    """view for updating a client record"""

    try:
        all = Client.objects.all().order_by("-id")
        pgs = Paginator(all, 7)
        pg_num = request.GET.get("page")
        client_list = pgs.get_page(pg_num)

        client = Client.objects.get(pk=client_id)

        form = ClientForm(request.POST or None, instance=client)
        if form.is_valid():
            form.save()
            return redirect("client")

        return render(
            request,
            "dashboard/update-client.html",
            {"form": form, "client": client, "content_list": client_list},
        )
    except IntegrityError as e:
        return render(request, "dashboard/not-working.html", {"error": e})


def delete_client(request, client_id):
    client = Client.objects.get(pk=client_id)

    # if request.user == request.user.is_authenticated:
    client.delete()
    return redirect("client")
    # return render(request, "dashboard/not-access.html")


def add_product(request):
    """view for creating a product"""
    products = Product.objects.all().order_by("id")

    pgs = Paginator(products, 7)
    pg_num = request.GET.get("page")
    product_list = pgs.get_page(pg_num)

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product")

    return render(
        request,
        "dashboard/add-product.html",
        {"form": ProductForm, "content_list": product_list},
    )


def update_product(request, product_id):
    """view for updating a product"""
    products = Product.objects.all().order_by("id")

    pgs = Paginator(products, 7)
    pg_num = request.GET.get("page")
    product_list = pgs.get_page(pg_num)

    item = Product.objects.get(pk=product_id)

    form = ProductForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect("product")

    return render(
        request,
        "dashboard/update-product.html",
        {"form": form, "item": item, "content_list": product_list},
    )


def delete_product(request, product_id):
    item = Product.objects.get(pk=product_id)
    if request.user == request.user.is_superuser:
        item.delete()
        return redirect("product")
    return render(request, "dashboard/not-access.html")


def mark_complete(request, contract_id):
    contract = Contract.objects.get(pk=contract_id)

    contract.status_id = "completed"
    contract.save()

    print(contract)
    return redirect("contract")


def redeem_product(request, contract_id):

    contract = Contract.objects.get(pk=contract_id)

    form = RedeemProductForm(request.POST or None, instance=contract)
    if form.is_valid():
        contract.status_id = "redeemed"
        contract.save()
        form.save()
        return redirect("contract")

    form = RedeemProductForm(instance=contract)
    context = {"contract": contract, "form": form}

    return render(request, "dashboard/redeem-product.html", context=context)


def create_contract(request):
    """view for creating a contract"""
    clients = Client.objects.all().order_by("-id")
    products = Product.objects.all().order_by("-id")
    branches = Branch.objects.all().order_by("-id")
    salesteam = Salesteam.objects.all().order_by("-id")
    todate = datetime.today()
    expires = todate + timedelta(days=90)
    status = "pending"
    # prform = Product.objects.all()
    contractform = ContractForm

    if request.method == "POST":
        client = request.POST["contract_client"]
        product = request.POST["contract_product"]
        price = request.POST["contract_price"]
        branch = request.POST["contract_branch"]
        sales = request.POST["contract_sales"]

        # print(client, product, price, branch, sales, expires, status)
        Contract.objects.create(
            price=price,
            expiry=expires,
            client_id=client,
            product_id=product,
            branch_id=branch,
            salesrep_id=sales,
            status_id=status,
        )

        # send text when new contract is opened
        new_contract_sms(client)

        return redirect("contract")

    return render(
        request,
        "dashboard/create-contract.html",
        {
            "form": contractform,
            "clients": clients,
            "products": products,
            "branches": branches,
            "salesteam": salesteam,
        },
    )


def add_client_contract(request):
    if request.method == "GET":
        id = request.GET["addclient_id"]
        name = request.GET["addclient_name"]
        msisdn = request.GET["addclient_msisdn"]

        Client.objects.create(
            id_number=id,
            name=name,
            msisdn=msisdn,
        )

        return redirect("create_contract")


def add_product_contract(request):
    if request.method == "GET":
        product = request.GET["addprod_item"]
        model = request.GET["addprod_model"]

        Product.objects.create(item=product, model=model)

        return redirect("create_contract")


def update_contract(request, client_id):
    """view for updating a contract record"""
    contract = Contract.objects.get(pk=client_id)
    # print(type(request.user), type(contract.salesrep.username))
    if str(request.user) == contract.salesrep.username or request.user.is_superuser:
        # use form only when method is POST
        form = UpdateContractForm(request.POST or None, instance=contract)
        if form.is_valid():
            form.save()
            return redirect("index")

        form = UpdateContractForm(instance=contract)
        print("form not submitted")

        context = {"contract": contract, "form": form}

        return render(
            request, "dashboard/update-contract.html", context=context
        )  # noqa
    return render(request, "dashboard/not-access.html")


def update_payment(request, payment_id):

    paid = Payment.objects.get(pk=payment_id)

    pass


def delete_payment(request, payment_id):
    paid = Payment.objects.get(pk=payment_id)

    paid.delete()
    return redirect("payment")


def record_bank(request):

    if request.method == "GET":

        bank_ref_id = request.GET["ref_id"]
        bank_amount = request.GET["bank_amount"]

        bank_account_name = request.GET["account_name"]
        contract = request.GET["contract_id"]
        bank_transfer_time = request.GET["transfer_time"]
        time_format = strptime(bank_transfer_time, "%Y-%m-%d %H:%M:%S")
        formatted = strftime("%d-%m-%Y %H:%M:%S", time_format)

        print(
            bank_ref_id,
            bank_amount,
            bank_transfer_time,
            bank_account_name,
            contract,
        )

        Payment.objects.create(
            bank_ref_id=bank_ref_id,
            bank_amount=bank_amount,
            bank_transfer_time=formatted,
            bank_account_name=bank_account_name,
            mode_id="bank transfer",
            contract_id=contract,
        )

        payment_sms(contract)

    return redirect("payment")


def record_cash(request):
    if request.method == "GET":

        cash = request.GET["cash_amount"]
        contract = request.GET["contract_ids"]
        time_paid = strftime("%d-%m-%Y %H:%M:%S")

        print(cash, time_paid, contract)

        pwc = Payment.objects.create(
            cash_amount=cash,
            cash_date_paid=time_paid,
            contract_id=contract,
        )

        pwc.mode_id = "cash"
        pwc.save()

        payment_sms(contract)

        return redirect("payment")


def contract_csv(request):
    """exporting csv file showing all contracts"""

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="contracts.csv"'},  # noqa
    )

    writer = csv.writer(response)

    contracts = Contract.objects.all()

    writer.writerow(
        [
            "Client",
            "Product",
            "Price",
            "Status",
            "Signed",
            "Expiry",
            "Salesrepresentative",
        ]
    )

    for contract in contracts:
        writer.writerow(
            [
                contract.client,
                contract.product,
                contract.price,
                contract.status,
                contract.created_at,
                contract.expiry,
                contract.salesrep,
            ]
        )

    return response


def payment_csv(request):
    """exporting csv file showing all payments"""

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="payments.csv"'},
    )

    writer = csv.writer(response)

    payments = Payment.objects.all()

    writer.writerow(
        [
            "No.",
            "Cash",
            "Cash Paid",
            "Till Transaction ID",
            "Till Amount",
            "Till Transaction Time",
            "Bank Reference ID",
            "Bank Amount",
            "Bank Transfer Time",
            "Bank Account Name",
        ]
    )

    for payment in payments:
        writer.writerow(
            [
                payment.id,
                payment.cash_amount,
                payment.cash_date_paid,
                payment.till_trans_id,
                payment.till_amount,
                payment.till_trans_time,
                payment.bank_ref_id,
                payment.bank_amount,
                payment.bank_transfer_time,
                payment.bank_account_name,
            ]
        )
    return response


def client_csv(request):
    """exporting csv file showing all clients"""

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="clients.csv"'},
    )

    writer = csv.writer(response)

    contacts = Client.objects.all()

    writer.writerow(
        [
            "Client",
            "National ID",
            "Mobile",
            "Registered On",
        ]
    )

    for contact in contacts:
        writer.writerow(
            [
                contact.name,
                contact.id_number,
                contact.msisdn,
                contact.created_at,
            ]
        )

    return response


# def send_text(request):
#     pending = list(Contract.objects.filter(status__standing__icontains="pending").values_list("client_id", flat=True))


#     mobile = list(Client.objects.filter(id__in=pending).values_list("msisdn", flat=True))


#     # print(pending)
#     # print(mobile)
#     sms(mobile)

#     pass
