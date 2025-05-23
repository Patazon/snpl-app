"""module providing for urls"""

from django.urls import path

from dashboard.views import add_client  # send_text,
from dashboard.views import (
    Index,
    add_client_contract,
    add_product,
    add_product_contract,
    client,
    client_csv,
    completed_contracts,
    contract,
    contract_csv,
    create_contract,
    delete_client,
    delete_payment,
    delete_product,
    mark_complete,
    payment,
    payment_csv,
    pending_contracts,
    product,
    record_bank,
    record_cash,
    record_mpesa,
    redeem_product,
    search,
    show_search,
    update_client,
    update_contract,
    update_product,
)

urlpatterns = [
    path("", Index, name="index"),
    # search
    path("search/", search, name="search"),
    path("search/<searched_id>", show_search, name="show_search"),
    # contract
    path("contracts/", contract, name="contract"),
    path("contract/create", create_contract, name="create_contract"),
    path("contract/update/<client_id>", update_contract, name="update_contract"),
    path("contracts/download", contract_csv, name="contract_csv"),
    path("contract/new_client", add_client_contract, name="add_client_contract"),
    path("contract/new_product", add_product_contract, name="add_product_contract"),
    path("contract/mark_complete/<contract_id>", mark_complete, name="mark_complete"),
    path(
        "contract/redeem_product/<contract_id>", redeem_product, name="redeem_product"
    ),
    path("contracts/completed", completed_contracts, name="completed_contracts"),
    path("contracts/pending", pending_contracts, name="pending_contracts"),
    # client
    path("clients/", client, name="client"),
    path("client/add", add_client, name="add_client"),
    path("client/update/<client_id>", update_client, name="update_client"),
    path("client/delete/<client_id>", delete_client, name="delete_client"),
    path("clients/download", client_csv, name="client_csv"),
    # payment
    path("payments/", payment, name="payment"),
    path("record_bank_transfer/", record_bank, name="record_bank"),
    path("record_cash/", record_cash, name="record_cash"),
    path("record_mpesa/", record_mpesa, name="record_mpesa"),
    path("payments/download", payment_csv, name="payment_csv"),
    path("payments/delete/<payment_id>", delete_payment, name="delete_payment"),
    # product
    path("products/", product, name="product"),
    path("product/add", add_product, name="add_product"),
    path("product/update/<product_id>", update_product, name="update_product"),
    path("product/delete/<product_id>", delete_product, name="delete_product"),
    # tilil
    # path("text/", send_text, name="send_text")
]
