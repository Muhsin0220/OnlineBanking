from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import User,Wallet,Transaction
from django.contrib.auth import authenticate
from .serializers import UserSerializer,TransactionSerializer,WalletSerializer
from random import randint
from rest_framework.authtoken.models import Token



@api_view(['POST'])
def register(request):
        username=request.data.get('username')
        password=request.data.get('password')
        first_name=request.data.get('first_name')
        try:
            user=User.objects.get(username=username)
            return Response({'message':'User already exist'})
        except User.DoesNotExist:
            otp =str(randint(100000,999999))
            print(otp)
            user=User(username=username,first_name=first_name,otp=otp)
            user.set_password(password)
            user.save()
            Token.objects.get_or_create(user=user)
            return Response({'message': 'User registered successfully.'})


@api_view(['POST'])
def verify_otp(request):
    username=request.data.get('username')
    otp=request.data.get('otp')
    
    try:
        user=User.objects.get(username=username,otp=otp)
        user.is_verified = True
        user.save()
        return Response({'message':'OTP verified successfully'})
    except User.DoesNotExist:
        return Response({'error':'Invalid OTP'})



@api_view(['POST'])
def login(request):
    username=request.data.get('username')
    password=request.data.get('password')    
    
    user=authenticate(request,username=username,password=password)

    if user and user.is_verified:
        serializer=UserSerializer(user)
        data=serializer.data
        try:
            data["token"] = Token.objects.get(user=user).key
        except:
            data["token"] = Token.objects.create(user=user).key
        return Response(data)
        # return Response({'message': 'Login successful'})
    return Response({'message': 'Invalid credentials'}, status=403)



@api_view(['POST'])
def forgetpassword(request):
    first_name=request.data.get('first_name')
    username=request.data.get('username')
    user=User.objects.get(username=username,first_name=first_name)
    if user:
        otp=str(randint(100000, 999999))
        print(otp)
        user.otp=otp
        user.save() 
        return Response({'message': 'OTP sent successfully'})
    else:
        return Response({'message': 'invalid cridential'})
    


@api_view(['POST'])
def changePassword(request):
    username=request.data.get('username')
    otp=request.data.get('otp')
    password=request.data.get('password1')
    confirm_password=request.data.get('password2')
    if password==confirm_password:
        user=User.objects.get(username=username,otp=otp)
        user.set_password(password)
        user.save()
        return Response({'message': 'Password changed'})
    else:
        return Response({'message': 'Error Found'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet_detail(request):
    username=request.user
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message':'User does not exist'},status=400)
    try:
        wallet=Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({'message':'Wallet does not exist for this user'},status=400)
    serializer=WalletSerializer(wallet)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAdminUser])
def wallet_update(request):
    username=request.data.get('username')
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message':'User does not exist'},status=400)
        
    try:
        wallet=Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({'message':'Wallet does not exist for this user'},status=400)
    new_amount=request.data.get('amount')
    wallet.amount=new_amount
    wallet.save()
        
    serializer=WalletSerializer(wallet)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transaction_create(request):
    sender=request.user
    receiver_username=request.data.get('receiver')
    amount=int(request.data.get('amount'))

    try:
        receiver=User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return Response({'error': 'Receiver does not exist'}, status=400)
    
    sender_wallet = Wallet.objects.get(user=sender)
    if sender_wallet.amount<amount:
        return Response({'error': 'Insufficient Balance'}, status=400)
    transaction = Transaction(sender=sender, receiver=receiver, amount=amount)
    transaction.save()

    sender_wallet.amount-=amount
    sender_wallet.save()
    receiver_wallet,created=Wallet.objects.get_or_create(user=receiver)
    receiver_wallet.amount+=amount
    receiver_wallet.save()
    return Response({'success':'Transaction successful'})
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_list(request):
    user=request.user
    try:
        user=User.objects.get(username=user)
    except User.DoesNotExist:
        return Response({'message':'User does not exist'},status=400)
    sent_transactions=Transaction.objects.filter(sender=user)
    received_transactions=Transaction.objects.filter(receiver=user)       
    sent_serializer=TransactionSerializer(sent_transactions,many=True)
    received_serializer=TransactionSerializer(received_transactions,many=True)
    return Response({'sent_transactions':sent_serializer.data,'received_transactions':received_serializer.data})