## All request functions for the API's
from __api__ import nsapi
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import yaml

with open('config.yaml') as file:
    config = yaml.full_load(file)
## NS API


def get_station(station):
    params = urllib.parse.urlencode({
        'q':  f'{station}',
        'limit': 8,
        'details': 'false',
        'lang': f'{ config["language"] }',
    })
    url = f"/places-api/v2/places"
    get_results = nsapi(url, params)
    stationcode_results = []
    for station in get_results['payload'][0]['locations']:
        stationcode_results.append(station['stationCode'])
    stationcode = min(stationcode_results, key=len)
    params = urllib.parse.urlencode({
        'station_code': f'{stationcode}',
        'limit': 1,
        'details': 'false',
        'lang': f'{config["language"]}',
    })
    station = nsapi(url, params)
    return station['payload'][0]['locations'][0]

def get_train(ridenumber):
    params = urllib.parse.urlencode({
    })
    url = f"/virtual-train-api/api/v1/trein/{ridenumber}"
    train = nsapi(url, params)
    if 'type' not in train:
        train['type'] = 'Onbekend'
        train['lengte'] = ''
    return train

def get_disruptions():
    url = f"/reisinformatie-api/api/v3/disruptions"
    params = urllib.parse.urlencode({
        'isActive': 'true',
    })
    disruptions = nsapi(url, params)
    return disruptions

##-----------------------------------------------------------------------------
## Wakatime API
##-----------------------------------------------------------------------------

def get_wakatime():
    url = f"api/v1/users/martvdm/projects/TrainAPI/stats"
    wakatime = wakatimeapi(url, params)
    print(wakatime)