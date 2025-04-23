"""module for serializing data from databases"""

from rest_framework import serializers

from daraja.models import CallbackResults, OAuthToken, TillTransaction, Transaction


class OAuthTokenSerializer(serializers.ModelSerializer):
    """serializes data from OAuthtoken database"""

    class Meta:
        """defines which model fields to serialize"""

        model = OAuthToken
        fields = "__all__"


class TillTransactionSerializer(serializers.ModelSerializer):
    """serializes data from TillTransaction database"""

    class Meta:
        """defines which model fields to serialize"""

        model = TillTransaction
        fields = "__all__"


class CallbackResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackResults
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
