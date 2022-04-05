import json
import http.client, urllib.request, urllib.parse, urllib.error, base64

with open("./config.json") as jsonfile:
    config = json.load(jsonfile)

def request_nsapi(url, params):
    headers = {
        'Ocp-Apim-Subscription-Key': f"{config['api']['NS-PRIMARY']}",
    }
    try:
        conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
        conn.request("GET", f"{url}?%s" % params, "{body}", headers)
        response = conn.getresponse()
        json_raw = response.read()
        json_data = json.loads(json_raw)
        conn.close()
    except Exception as e:
        print('Het ophalen van de API is mislukt. Probeer het later opnieuw.')
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return json_data

def get_station(station):
    params = urllib.parse.urlencode({
        'q':  f'{station}',
        'limit': 8,
        'details': 'false',
        'lang': f'{ config["language"] }',
    })
    url = f"/places-api/v2/places"
    get_results = request_nsapi(url, params)
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
    station = request_nsapi(url, params)
    return station['payload'][0]['locations'][0]

def get_train(ridenumber):
    params = urllib.parse.urlencode({
    })
    url = f"/virtual-train-api/api/v1/trein/{ridenumber}"
    train = request_nsapi(url, params)
    if 'type' not in train:
        train['type'] = 'Onbekend'
        train['lengte'] = ''
    return train
