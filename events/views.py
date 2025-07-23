
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
def update_event(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
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

