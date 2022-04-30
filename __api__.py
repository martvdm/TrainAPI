import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
import yaml

with open('config.yaml') as file:
    config = yaml.full_load(file)

def nsapi(url, params):
    headers = {
        'Ocp-Apim-Subscription-Key': f"{config['api']['ns-primary-key']}",
    }
    try:
        conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
        conn.request("GET", f"{url}?%s" % params, "{body}", headers)
        response = conn.getresponse()
        json_raw = response.read()
        json_data = json.loads(json_raw)
        conn.close()
    except Exception as e:
        print('Error: %s' % e)
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return json_data

def githubapi(url, params):
    
    return
