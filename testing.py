import requests
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import json, xmltodict, yaml

data_resp = []

def csv_to_json(data):
    tempDec = {}
    json_data = []
    rows = data['data'].split("\n")
    keys = rows.pop(0).split(",")
    for i in range(len(rows)):
        rows[i] = rows[i].split(",")
    for i in range(len(rows)-1):
        for j in range(len(keys)):
            tempDec[keys[j]] = rows[i][j]
        json_data.append(json.loads(json.dumps(tempDec)))
    return json_data

def to_common_data_type(data):
    if 'mime_type' in data:
        if data['mime_type'] == 'application/xml':
            for dt in json.loads(json.dumps(xmltodict.parse(data['data'])))['dataset']['record']:
                data_resp.append(dt)
        elif data['mime_type'] == 'text/csv':
            for dt in (csv_to_json(data)):
                data_resp.append(dt)
        elif data['mime_type'] == 'application/x-yaml':
            for dt in json.loads(json.dumps(yaml.safe_load(data['data']))):
                data_resp.append(dt)
    else:
        tmp = str(data['data'])
        # FCINKG COMMA
        if tmp[len(tmp)-3] == ',':
            tmp = tmp[0:-3]
            tmp = tmp + ']'            
        for dt in json.loads(tmp):
            data_resp.append(dt)   
    return

def make_request(route, access_token, base_url):
    response = requests.get(base_url + route, headers={'X-Access-Token' : access_token})
    to_common_data_type(json.loads(response.text))
    next_routes = []
    if 'link' in response.json():
        for link in response.json()['link'].values():
            next_routes.append(link)        
    return next_routes

def main():
    futures, executor, access_token, base_url = start_point()
    while futures:
        done, futures = wait(futures, return_when=FIRST_COMPLETED)
        for future in done:
            if future:
                for link in future.result():
                    futures.add(executor.submit(make_request, link, access_token, base_url))

def start_point():
    base_url = 'http://localhost:5000'
    register_req = requests.get(base_url + '/register').json()
    base_request = requests.get(base_url +  register_req['link'], headers={'X-Access-Token' : register_req['access_token']}).json()

    executor = ThreadPoolExecutor(max_workers=6)
    futures = []
    for route in base_request['link'].values():
        futures.append(executor.submit(make_request, route, register_req['access_token'], base_url))
    return futures, executor, register_req['access_token'], base_url

if __name__ == "__main__":
    main()
    print(data_resp)
