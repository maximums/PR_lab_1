import requests
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import json, xmltodict, csv, yaml

data_resp = []

def csv_to_dic(data):
    tempDec = {}
    json_data = []
    rows = data['data'].split("\n")
    keys = rows.pop(0).split(",")
    for i in range(len(rows)):
        rows[i] = rows[i].split(",")
    for i in range(len(rows)-1):
        for j in range(len(keys)):
            tempDec[keys[j]] = rows[i][j]
        json_data.append(json.dumps(tempDec))
    return json_data

def to_common_data_type(data):
    if 'mime_type' in data:
        if data['mime_type'] == 'application/xml':
            data_resp.append(json.dumps(xmltodict.parse(data['data'])))
        elif data['mime_type'] == 'text/csv':
            data_resp.append(csv_to_dic(data))
        elif data['mime_type'] == 'application/x-yaml':
            data_resp.append(json.dumps(yaml.safe_load(data['data']))) 
    else:
        data_resp.append(data)    
    return

def make_request(route, access_token, base_url):
    response = requests.get(base_url + route, headers={'X-Access-Token' : access_token}).json()
    # data_resp.append(response)
    to_common_data_type(response)
          
    next_routes = []
    if 'link' in response:
        for link in response['link'].values():
            next_routes.append(link)        
    return next_routes

def main(args):
    while args[0]:
        done, args[0] = wait(args[0], return_when=FIRST_COMPLETED)
        for future in done:
            if future:
                for link in future.result():
                    args[0].add(args[1].submit(make_request, link, args[2], args[3]))

def start_point():
    base_url = 'http://localhost:5000'
    register_req = requests.get(base_url + '/register').json()
    base_request = requests.get(base_url +  register_req['link'], headers={'X-Access-Token' : register_req['access_token']}).json()

    e = ThreadPoolExecutor(max_workers=6)
    futures = {
        e.submit(make_request, link, register_req['access_token'], base_url) : link for link in base_request['link'].values()
    }
    return [futures, e, register_req['access_token'], base_url]

if __name__ == "__main__":
    main(start_point())
    for date in data_resp:
        print(date)

