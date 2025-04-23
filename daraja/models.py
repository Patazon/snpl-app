"""module providing for models and their schema"""

from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class AbstractBaseModel(models.Model):
    """defining a base model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """provides inheritance"""

        abstract = True


class OAuthToken(AbstractBaseModel):
    """model for token"""

    token = models.CharField(max_length=100)
    expiry = models.CharField(max_length=5)

    def __str__(self):
        return str(self.token)


class TillTransaction(AbstractBaseModel):
    """model for till transactions"""

    body = models.JSONField()

    def __str__(self):
        return str(self.body)


class CallbackResults(AbstractBaseModel):
    body = models.JSONField()

    def __str__(self):
        return str(self.body)


class Transaction(AbstractBaseModel):
    msisdn = models.CharField(max_length=20)
    amount = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    receipt_number = models.CharField(max_length=100)
    time = models.CharField(max_length=50)

    def __str__(self):
        return str(self.receipt_number)
