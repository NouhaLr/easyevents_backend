
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import ListCreateAPIView
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    if request.user.role != 'admin':
        return Response({"detail": "Not authorized"}, status=403)
    
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # change if needed

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # change if needed
from rest_framework.decorators import api_view, permission_classes

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    print("Received data:", request.data)  # 👈 Ajoute ceci pour debug

    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        print("Serializer errors:", serializer.errors)  # 👈 Ajoute ceci
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'detail': 'Event not found'}, status=404)

    if request.user.role != 'admin':
        return Response({'detail': 'Not authorized'}, status=403)

    event.delete()
    return Response({'detail': 'Event deleted successfully'}, status=204)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    user = request.user
    data = request.data
    data['user'] = user.id

    if Reservation.objects.filter(user=user, event=data['event']).exists():
        return Response({'detail': 'You have already reserved for this event.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReservationSerializer(data=data)
    if serializer.is_valid():
        reservation = serializer.save(user=user)

        event_id = reservation.event.id
        count = Reservation.objects.filter(event=reservation.event).count()
        reservation.receipt_number = f"RECEIPT-{event_id}-{count:04d}"
        reservation.save()

        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_reservation(request, event_id):
    try:
        reservation = Reservation.objects.get(user=request.user, event__id=event_id)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
    except Reservation.DoesNotExist:
        return Response({'reserved': False})


