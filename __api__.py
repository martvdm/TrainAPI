import json
import http.client, urllib.request, urllib.parse, urllib.error, base64

with open("config.json") as jsonfile:
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
        'q':  f'station {station}',
        'limit': '1',
        'lang': f'{ config["language"] }',
    })
    url = f"/places-api/v2/places"
    get_stations = request_nsapi(url, params)
    return get_stations['payload'][0]['locations'][0]

def get_train(ridenumber):
    params = urllib.parse.urlencode({
    })
    url = f"/virtual-train-api/api/v1/trein/{ridenumber}"
    train = request_nsapi(url, params)
    if 'type' not in train:
        train['type'] = 'Onbekend'
        train['lengte'] = ''
    return train
