from rest_framework import serializers
from  .models import Merchant


class MerchantSerializer(serializers.ModelSerializer):
    user_full_name=serializers.ReadOnlyField()

    class Meta:
        model=Merchant
        fields=['id','name','b2c_shortcode','c2b_shortcode','charges_paid_account_balance','organisation_account_balance',
                 'utility_account_balance','working_account_balance','deposits_ipn_url','payouts_ipn_url','user',
                 'user_full_name','app_key','app_secret',
                 ]


