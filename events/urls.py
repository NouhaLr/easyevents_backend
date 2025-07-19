from django.urls import path
from .views import create_event,EventListCreateView


urlpatterns = [   
    path('create/', create_event),
    path('list/', EventListCreateView.as_view(), name='events'),
    ]