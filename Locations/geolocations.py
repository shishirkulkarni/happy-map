from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient

def get_latlng(address):

    google_maps = GoogleMaps(api_key='AIzaSyCcuF3AbW0iS9QChjdMUsstXN7C5zOJ5gg')

    location = google_maps.search(location=address)

    my_location = location.first()

    return(str(my_location.lat), str(my_location.lng))


addresses = [
             'Salt Lake City, UT',
             'Kansas City, KS',
             'Columbus, OH',
             'Indianapolis, IN',
             'San Antonio, TX',
             'Las Vegas, NV',
             'Cincinnati, OH']

file_geolocations =  open('geolocations5.tsv', 'w')

file_geolocations.write('location_name\tlat\tlong\n')

for address in addresses:
    lat_lng = get_latlng(address)
    file_geolocations.write(address + '\t' + lat_lng[0] + '\t' + lat_lng[1] + '\n')

