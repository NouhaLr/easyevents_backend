from django.urls import path
from .views import create_event,EventListCreateView, update_event, delete_event, create_reservation, get_user_reservation

urlpatterns = [   
    path('create/', create_event),
    path('list/', EventListCreateView.as_view(), name='events'),
    path('update/<int:pk>/', update_event),
    path('delete/<int:pk>/', delete_event),
    path('reservations/', create_reservation, name='create_reservation'),
    path('reservations/<int:event_id>/',get_user_reservation, name='get_user_reservation'),
   
    ]