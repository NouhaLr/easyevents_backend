from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet, Transaction
from events.models import Event
from .serializers import WalletSerializer, TransactionSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data)

from decimal import Decimal, InvalidOperation

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recharge_wallet(request):
    amount = request.data.get('amount')
    if amount is None:
        return Response({'detail': 'Amount is required'}, status=400)

    try:
        amount = Decimal(amount)  # convertit en Decimal
    except (InvalidOperation, ValueError):
        return Response({'detail': 'Invalid amount format'}, status=400)

    if amount <= 0:
        return Response({'detail': 'Amount must be positive'}, status=400)

    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    wallet.balance += amount  # ici c'est Decimal + Decimal
    wallet.save()

    return Response({'detail': 'Wallet recharged successfully', 'balance': float(wallet.balance)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_transaction(request):
    event_id = request.data.get('event_id')
    amount = float(request.data.get('amount'))
    description = request.data.get('description', '')

    try:
        event = Event.objects.get(id=event_id)
        wallet = Wallet.objects.get(user=request.user)

        if wallet.balance < amount:
            return Response({'detail': 'Insufficient balance'}, status=400)

        wallet.balance -= amount
        wallet.save()

        tx = Transaction.objects.create(wallet=wallet, event=event, amount=amount, description=description)
        return Response(TransactionSerializer(tx).data, status=201)

    except Event.DoesNotExist:
        return Response({'detail': 'Event not found'}, status=404)
