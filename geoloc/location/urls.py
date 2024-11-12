from django.urls import path
from location.views import save_user_geolocation, view_user_geolocation, user_locations_map, get_location, user_list, user_location_history

urlpatterns = [
    path('abc/', save_user_geolocation, name='save_user_geolocation'),
    path('xyz/', get_location, name='get_location'),
    path('view/', view_user_geolocation, name='view_user_geolocation'),
    path('map/', user_locations_map, name='user_locations_map'),
    path('users/', user_list, name='user_list'),
    path('user/<int:user_id>/', user_location_history, name='user_location_history')
]
