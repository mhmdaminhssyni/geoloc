from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from location.models import UserGeoLocation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Max
@csrf_exempt  # Disable CSRF for development only; remove in production.
def save_user_geolocation(request):
    if request.method == 'POST':
        latitude = request.POST.get('lat')
        longitude = request.POST.get('long')

        if latitude is None or longitude is None:
            return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)

        if request.user.is_authenticated:
            # Create a new entry each time
            UserGeoLocation.objects.create(
                user=request.user,
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({'status': 'Geolocation saved successfully'})
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

    return JsonResponse({'error': 'Invalid request method, POST required'}, status=405)

def get_location(request):
    return render(request, 'location/form.html')

@login_required
def view_user_geolocation(request):
    # Retrieve all locations for the logged-in user, ordered by timestamp
    user_locations = UserGeoLocation.objects.filter(user=request.user).order_by('-timestamp')

    if not user_locations.exists():
        context = {
            'error': 'Location not found for this user.'
        }
    else:
        context = {
            'locations': user_locations  # Pass all locations to the template
        }

    return render(request, 'location/view_location.html', context)


def user_locations_map(request):
    user_locations = UserGeoLocation.objects.filter(user=request.user)
    context = {
    'locations': list(user_locations.values('latitude', 'longitude'))
    }
    return render(request, 'location/map.html', context)

@login_required
def user_list(request):
    users_with_locations = User.objects.filter(usergeolocation__isnull=False).distinct()
    context = {'users': users_with_locations}
    return render(request, 'location/user_list.html', context=context)

@login_required
def user_location_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    locations = UserGeoLocation.objects.filter(user=user).order_by('timestamp')  
    context = {'user': user, 'locations': locations}
    return render(request, 'location/user_location_history.html', context=context)