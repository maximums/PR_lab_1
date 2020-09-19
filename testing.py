import requests
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

data_resp = []

def make_request(route, access_token, base_url):
    response = requests.get(base_url + route, headers={'X-Access-Token' : access_token}).json()
    data_resp.append(response)
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
    
    e = ThreadPoolExecutor(max_workers=12)
    futures = {
        e.submit(make_request, link, register_req['access_token'], base_url) : link for link in base_request['link'].values()
    }
    return [futures, e, register_req['access_token'], base_url]

if __name__ == "__main__":
    main(start_point())
    for date in data_resp:
        print(date)

