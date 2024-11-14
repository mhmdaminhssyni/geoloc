from django.urls import path
from location.views import (
    save_user_geolocation, 
    view_user_geolocation, 
    user_list, 
    user_location_history, 
    user_location_map,
    signup
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('geolocation/save/', save_user_geolocation, name='save_user_geolocation'),
    path('geolocation/view/', view_user_geolocation, name='view_user_geolocation'),
    path('users/', user_list, name='user_list'),
    path('user/<int:user_id>/locations/', user_location_history, name='user_location_history'),
    path('user/<int:user_id>/location/<str:timestamp>/', user_location_map, name='user_location_map')
]