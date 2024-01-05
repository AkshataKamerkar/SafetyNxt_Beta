from geopy.geocoders import Nominatim

'''
    This file will contain all the functions that are used in backend for user input manipulation as well as to fetch the appropriate cctv id's

'''


# Get ll's from loc


def get_latitude_longitude(place_name):
    geolocator = Nominatim(user_agent="geoapiExercises")

    location = geolocator.geocode(place_name)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return [latitude, longitude]
    else:
        return [None, None]


# Getting location from the ll's
def get_location(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="location_app")
        location = geolocator.reverse(f"{latitude}, {longitude}", language='en')
        return location.address if location else "Location not found."
    except Exception as e:
        return f"Error: {str(e)}"
