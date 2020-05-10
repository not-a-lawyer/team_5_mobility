import requests
from flask import Flask, render_template

from python_logic import compute_overall_trip_time

URL = "https://geocode.search.hereapi.com/v1/geocode"
departure = 'Berlin Hauptbahnhof'  # taking user input
goal = 'Lohmühlenstraße 65'
parking = 'Karl-Kunger-Straße 54'
##INSERT OWN KEY HERE###
api_key = ''  # Acquire from developer.here.com
PARAMS = {'apikey': api_key, 'q': departure}
PARAMS_end = {'apikey': api_key, 'q': goal}
PARAMS_parking = {'apikey': api_key, 'q': parking}

# sending get request and saving the response as response object
r_start = requests.get(url=URL, params=PARAMS)
r_end = requests.get(url=URL, params=PARAMS_end)
r_park = requests.get(url=URL, params=PARAMS_parking)

intermodal_route = requests.get(
    'https://intermodal.router.hereapi.com/v8/routes?apikey='+api_key+'&alternatives=2&destination=52.40358749909618,13.058351363288239&origin=52.53105637575095,13.384944833815183')
data = intermodal_route.json()
departure_data = r_start.json()
end_data = r_end.json()
park_data = r_park.json()
print(data['routes'][0]['sections'][0]['departure']['place']['location']['lat'])

# Acquiring the latitude and longitude from JSON
# latitude = data['routes'][0]['sections'][0]['departure']['place']['location']['lat']
start_latitude = departure_data['items'][2]['position']['lat']
end_latitude = end_data['items'][0]['position']['lat']
park_latitude = park_data['items'][0]['position']['lat']

# print(latitude)
start_longitude = departure_data['items'][2]['position']['lng']
end_longitude = end_data['items'][0]['position']['lng']
park_longitude = park_data['items'][0]['position']['lng']

URL_intermodal = 'https://intermodal.router.hereapi.com/v8/routes'
PARAMS_intermodal_all = {'destination': str(end_latitude) + ',' + str(end_longitude),
                         'origin': str(start_latitude) + ',' + str(start_longitude),
                         'apikey': api_key}

PARAMS_intermodal_park_and_ride = {'destination': str(end_latitude) + ',' + str(end_longitude),
                                   'origin': str(start_latitude) + ',' + str(start_longitude),
                                   'apikey': api_key,
                                   'alternatives': 3,
                                   'vehicle[modes]': 'car',
                                   'vehicle[enable]': 'routeHead',
                                   'transit[enable]': 'routeTail',
                                   'rented[enable]': '``'}

r_intermodal = requests.get(url=URL_intermodal, params=PARAMS_intermodal_all)
r_park_and_ride = requests.get(url=URL_intermodal, params=PARAMS_intermodal_park_and_ride)

real_modal_data = r_intermodal.json()
pr_modal = r_park_and_ride.json()

compute_overall_trip_time(real_modal_data)
pr_modal_time = compute_overall_trip_time(pr_modal)

# print(longitude)

r_car = requests.get(url='https://route.ls.hereapi.com/routing/7.2/calculateroute.json', params={'apikey': api_key,
                                                                                                 'waypoint0': str(
                                                                                                     start_latitude) + ',' + str(
                                                                                                     start_longitude),
                                                                                                 'waypoint1': str(
                                                                                                     end_latitude) + ',' + str(
                                                                                                     end_longitude),
                                                                                                 'mode':'fastest;car;traffic:enabled'
                                                                                                 })

car_data = r_car.json()

r_bike = requests.get(url='https://route.ls.hereapi.com/routing/7.2/calculateroute.json', params={'apikey': api_key,
                                                                                                 'waypoint0': str(
                                                                                                     start_latitude) + ',' + str(
                                                                                                     start_longitude),
                                                                                                 'waypoint1': str(
                                                                                                     end_latitude) + ',' + str(
                                                                                                     end_longitude),
                                                                                                 'mode':'fastest;bicycle'
                                                                                                 })

bike_data = r_bike.json()

r_parking_api = requests.get(url='https://osp.cit.cc.api.here.com/parking/segments', params={'apikey': api_key,
                                                                                             'bbox':str(
                                                                                               end_latitude) + ',' + str(
                                                                                                     end_longitude)+','+str(park_latitude) + ',' + str(
                                                                                              park_longitude)})

parking_data = r_parking_api.json()
# Flask code
app = Flask(__name__)


"""@app.route('/')
def map_func():
    return render_template('map.html', apikey=api_key, start_lat=start_latitude, start_lng=start_longitude,
                           end_longitude=end_longitude, end_latitude=end_latitude)  # map.html is my HTML file name
"""

@app.route('/')
def route_func():
    return render_template( 'route.html', apikey=api_key, origin=str(start_latitude) + ',' + str(start_longitude),
                           destination=str(end_latitude) + ',' + str(end_longitude))  #

@app.route('/isoling')
def isoling_func():
    return render_template('isoling.html', apikey=api_key, origin=str(start_latitude) + ',' + str(start_longitude))  #


if __name__ == '__main__':
    app.run(debug=False)
