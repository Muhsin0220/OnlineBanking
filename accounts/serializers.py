from rest_framework import serializers
from .models import User,Wallet,Transaction

# ,TransactionHistory
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','password','otp','is_verified')
        extra_kwargs={'password':{'write_only':True}}


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields='__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'