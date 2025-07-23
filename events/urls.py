from django.urls import path
from .views import create_event,EventListCreateView, update_event, delete_event


urlpatterns = [   
    path('create/', create_event),
    path('list/', EventListCreateView.as_view(), name='events'),
    path('update/<int:pk>/', update_event),
    path('delete/<int:pk>/', delete_event),
    ]