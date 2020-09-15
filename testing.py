import requests
import concurrent.futures

base_url = 'http://localhost:5000'
base_request = requests.get(base_url + '/register').json()
access_token = base_request['access_token']
r1 = requests.get(base_url + base_request['link'], headers = {'X-Access-Token': access_token})
def make_requests(next_route):
    req = requests.get(base_url + next_route, headers = {'X-Access-Token': access_token})
    print(req.json())
    if 'link' in req.json():
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
            for next_route in req.json()['link'].values():
                e.submit(make_requests, next_route)
    print('\n')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for next_route in r1.json()['link'].values():
        executor.submit(make_requests, next_route)
            