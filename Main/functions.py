import geocoder

'''
    This file will contain all the functions that are used in backend for user input manipulation as well as to fetch the appropriate cctv id's

'''


# Get ll's from loc
def get_latitude_longitude(locations):
    '''
    :param locations: List containing two place names or addresses entered by the user
    :return: List containing [latitude, longitude] of each specified place
    '''
    geolocator = Nominatim(user_agent="my_geocoder")  # Create a geolocator object
    coordinates_list = []

    for place in locations:
        location = geolocator.geocode(place)  # Use geocode() to get the location data
        if location is not None:
            latitude, longitude = location.latitude, location.longitude
            coordinates_list.append((latitude, longitude))
        else:
            print("Could not find the location:", place)
            coordinates_list.append(None)

    return coordinates_list

# Getting location from the ll's
def get_location(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="location_app")
        location = geolocator.reverse(f"{latitude}, {longitude}", language='en')
        return location.address if location else "Location not found."
    except Exception as e:
        return f"Error: {str(e)}"
