from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from location.models import UserGeoLocation, UserToken
from django.shortcuts import render, get_object_or_404

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if not username or not password or not email:
        return Response({'error': 'Username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)

    refresh = RefreshToken.for_user(user)
    UserToken.objects.create(
        user=user,
        refresh_token=str(refresh),
        access_token=str(refresh.access_token)
    )
    
    return Response({
        'message': 'User created successfully.',
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_user_geolocation(request):
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    if not latitude or not longitude:
        return Response({'error': 'Latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

    UserGeoLocation.objects.create(
        user=request.user,
        latitude=latitude,
        longitude=longitude
    )
    return Response({'status': 'Geolocation saved successfully'}, status=status.HTTP_200_OK)
    print(f"{latitude},{longitude}")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_user_geolocation(request):
    user_locations = UserGeoLocation.objects.filter(user=request.user).order_by('-timestamp')
    data = [{'latitude': loc.latitude, 'longitude': loc.longitude, 'timestamp': loc.timestamp} for loc in user_locations]
    return Response({'locations': data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    users_with_locations = User.objects.filter(usergeolocation__isnull=False).distinct()
    data = [{'id': user.id, 'username': user.username} for user in users_with_locations]
    return Response({'users': data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_location_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    locations = UserGeoLocation.objects.filter(user=user).order_by('timestamp')
    data = [{'latitude': loc.latitude, 'longitude': loc.longitude, 'timestamp': loc.timestamp} for loc in locations]
    return Response({'user': user.username, 'locations': data}, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def user_location_map(request, user_id, timestamp):
    user = get_object_or_404(User, id=user_id)
    location = UserGeoLocation.objects.filter(user=user, timestamp=timestamp).first()
    if not location:
        return Response({'error': 'No location found for this timestamp.'}, status=status.HTTP_404_NOT_FOUND)
    return render(request, 'location/map.html', {'latitude': location.latitude, 'longitude': location.longitude, 'timestamp': location.timestamp})
