import json
import requests
from tcpserver import server as tcp_ser
from parsedata import to_common_data_type as data_merge
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

def make_request(route, access_token, base_url):
    response = requests.get(base_url + route, headers={'X-Access-Token' : access_token})
    final_data = []
    final_data.extend(data_merge(json.loads(response.text)))
    next_routes = []
    if 'link' in response.json():
        for link in response.json()['link'].values():
            next_routes.append(link)        
    return next_routes, final_data

def main():
    futures, executor, access_token, base_url = start_point()
    final_data = []
    while futures:
        done, futures = wait(futures, return_when=FIRST_COMPLETED)
        for future in done:
            final_data.extend(future.result()[1])
            if future:
                for link in future.result()[0]:
                    futures.add(executor.submit(make_request, link, access_token, base_url))
    return final_data

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
    tcp_ser('localhost', 5001, main())
