from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from location.models import UserGeoLocation
from django.contrib.auth.decorators import login_required


@csrf_exempt  # Disable CSRF for development only; remove in production.
def save_user_geolocation(request):
    if request.method == 'POST':
        latitude = request.POST.get('lat')
        longitude = request.POST.get('long')

        if latitude is None or longitude is None:
            return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)

        if request.user.is_authenticated:
            UserGeoLocation.objects.create(
                user=request.user,
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({'status': 'Geolocation saved successfully'})
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

    # Respond with a message if it's not a POST request
    return JsonResponse({'error': 'Invalid request method, POST required'}, status=405)


def get_location(request):
    return render(request, 'location/form.html')

@login_required  # Ensures the user is logged in
def view_user_geolocation(request):
    try:
        # Retrieve the logged-in user's location
        user_location = UserGeoLocation.objects.get(user=request.user)
        context = {
            'latitude': user_location.latitude,
            'longitude': user_location.longitude
        }
    except UserGeoLocation.DoesNotExist:
        # Handle case where the user has no location saved
        context = {
            'error': 'Location not found for this user.'
        }

    return render(request, 'location/view_location.html', context)

def user_locations_map(request):
    user_locations = UserGeoLocation.objects.filter(user=request.user)
    context = {
    'locations': list(user_locations.values('latitude', 'longitude'))
    }
    return render(request, 'location/map.html', context)