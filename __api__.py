import json
import http.client, urllib.request, urllib.parse, urllib.error, base64

with open("config.json") as jsonfile:
    config = json.load(jsonfile)

def request_nsapi(type, params, api):

    headers = {
        'Ocp-Apim-Subscription-Key': f"{config['api']['NS-PRIMARY']}",
    }
    try:
        conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
        conn.request("GET", f"/{api}/v2/{type}?%s" % params, "{body}", headers)
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
    api = 'places-api'
    type = 'places'
    get_stations = request_nsapi(type, params, api)
    return get_stations['payload'][0]['locations'][0]