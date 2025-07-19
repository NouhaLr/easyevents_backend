
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import ListCreateAPIView

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