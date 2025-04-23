# Create your models here.
from django.db import models


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Branch(CommonInfo):
    branch = models.CharField(max_length=75, null=False, unique=True)

    class Meta:
        db_table = '"branches"'

    def __str__(self):
        return str(self.branch)


class Salesteam(CommonInfo):
    representative = models.CharField(max_length=75, null=False, unique=True)
    username = models.CharField(max_length=25, null=True, blank=True)
    branch = models.ForeignKey(
        Branch, db_column="branch", to_field="id", on_delete=models.CASCADE, default=1
    )

    class Meta:
        db_table = '"salesteams"'

    def __str__(self):
        return str(self.representative)


class PaymentMode(CommonInfo):
    mode = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        db_table = '"payment_modes"'

    def __str__(self):
        return str(self.mode)


class ContractStatus(CommonInfo):
    standing = models.CharField(max_length=30, null=False, unique=True)

    class Meta:
        db_table = '"contract_status"'

    def __str__(self):
        return str(self.standing)


class Client(CommonInfo):
    id_number = models.PositiveBigIntegerField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=75, null=False)
    msisdn = models.IntegerField(null=False)

    class Meta:
        db_table = '"clients"'

    def __str__(self):
        return str(self.id_number)


class Product(CommonInfo):
    item = models.CharField(max_length=250, null=False, unique=True)
    model = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = '"products"'

    def __str__(self):
        return str(self.item)


class Contract(CommonInfo):
    price = models.PositiveIntegerField(null=False)
    expiry = models.DateTimeField(null=False)

    client = models.ForeignKey(
        Client, db_column="client", to_field="id_number", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, db_column="product", to_field="item", on_delete=models.CASCADE
    )
    branch = models.ForeignKey(
        Branch, db_column="branch", to_field="branch", on_delete=models.CASCADE
    )
    salesrep = models.ForeignKey(
        Salesteam,
        db_column="salesrep",
        to_field="representative",
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        ContractStatus,
        db_column="status",
        to_field="standing",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = '"contracts"'

    def __str__(self):
        return str(self.client)


class Payment(CommonInfo):
    cash_amount = models.PositiveIntegerField(null=True, blank=True)
    cash_date_paid = models.CharField(max_length=75, blank=True, null=True)

    till_trans_id = models.CharField(max_length=75, blank=True, null=True)
    till_amount = models.PositiveIntegerField(blank=True, null=True)
    till_trans_time = models.CharField(max_length=75, blank=True, null=True)

    bank_ref_id = models.CharField(max_length=75, blank=True, null=True)
    bank_amount = models.PositiveIntegerField(blank=True, null=True)
    bank_transfer_time = models.CharField(max_length=75, blank=True, null=True)
    bank_account_name = models.CharField(max_length=75, blank=True, null=True)

    mode = models.ForeignKey(
        "PaymentMode",
        db_column="mode",
        to_field="mode",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    contract = models.ForeignKey(
        Contract,
        db_column="contract",
        to_field="id",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = '"payments"'

    def __str__(self):
        return str(self.mode)
