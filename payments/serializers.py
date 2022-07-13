from rest_framework import serializers
from  .models import Transaction




class TransactionSerializer(serializers.ModelSerializer):
    transaction_type_name=serializers.ReadOnlyField()

    class Meta:
        model=Transaction
        fields='__all__'



