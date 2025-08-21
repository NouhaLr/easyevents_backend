from django.shortcuts import render

# Create your views here.
# rfid/views.py
from decimal import Decimal, InvalidOperation
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction as db_transaction

from .models import Bracelet
from .serializers import BraceletAssignSerializer, BraceletSerializer

from wallet.models import Wallet, Transaction
from events.models import Event, Reservation


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_bracelet(request):
    """
    Admin (or staff at reception) assigns a tag UID to a reservation using the receipt number.
    """
    serializer = BraceletAssignSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    receipt_number = serializer.validated_data['receipt_number']
    tag_uid = serializer.validated_data['tag_uid'].strip()

    try:
        reservation = Reservation.objects.select_related('user', 'event').get(receipt_number=receipt_number)
    except Reservation.DoesNotExist:
        return Response({'detail': 'Reservation not found for that receipt number.'}, status=404)

    # Optional: restrict who can assign (e.g., only admins). For now, let any authenticated user.
    # if request.user.role != 'admin': return Response({'detail': 'Not authorized'}, status=403)

    # Prevent duplicate tag assignment
    if Bracelet.objects.filter(tag_uid=tag_uid).exists():
        return Response({'detail': 'This tag UID is already assigned.'}, status=400)

    # Ensure one bracelet per reservation (delete or update if reassign)
    bracelet, created = Bracelet.objects.get_or_create(reservation=reservation, defaults={'tag_uid': tag_uid})
    if not created:
        bracelet.tag_uid = tag_uid
        bracelet.active = True
        bracelet.save()

    return Response(BraceletSerializer(bracelet).data, status=201 if created else 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simulate_scan_purchase(request):
    """
    Simulate a reader scan that charges a purchase to the wallet:
    payload: { "tag_uid": "...", "event_id": 1, "amount": "12.50", "description": "Burger + Soda" }
    """
    tag_uid = request.data.get('tag_uid', '').strip()
    event_id = request.data.get('event_id')
    amount_raw = request.data.get('amount')
    description = request.data.get('description', '')

    if not tag_uid or not event_id or amount_raw in (None, ''):
        return Response({'detail': 'tag_uid, event_id and amount are required.'}, status=400)

    try:
        amount = Decimal(str(amount_raw))
        if amount <= 0:
            return Response({'detail': 'Amount must be positive.'}, status=400)
    except (InvalidOperation, TypeError, ValueError):
        return Response({'detail': 'Invalid amount.'}, status=400)

    try:
        bracelet = Bracelet.objects.select_related('reservation__user', 'reservation__event').get(tag_uid=tag_uid, active=True)
    except Bracelet.DoesNotExist:
        return Response({'detail': 'Active bracelet not found for this tag UID.'}, status=404)

    # Check event
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'detail': 'Event not found.'}, status=404)

    # OPTIONAL rule: only allow purchases against the event the bracelet belongs to.
    # If you want to enforce it, uncomment:
    if bracelet.reservation.event_id != event.id:
        return Response({'detail': 'Bracelet is not valid for this event.'}, status=400)

    user = bracelet.reservation.user

    # Wallet deduct + record transaction atomically
    with db_transaction.atomic():
        wallet, _ = Wallet.objects.select_for_update().get_or_create(user=user)
        if wallet.balance < amount:
            return Response({'detail': 'Insufficient balance.'}, status=400)
        wallet.balance = wallet.balance - amount
        wallet.save()

        tx = Transaction.objects.create(
            wallet=wallet,
            event=event,
            amount=amount,
            description=description
        )

    return Response({
        'detail': 'Purchase recorded.',
        'new_balance': str(wallet.balance),
        'transaction_id': tx.id,
        'event': event.name,
        'amount': str(amount),
        'description': tx.description
    }, status=201)
