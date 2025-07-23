from django.urls import path
from .views import RegisterView, MeView
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import MyTokenObtainPairView, check_email_exists
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',  MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('check-email/', check_email_exists, name='check_email'),

]
