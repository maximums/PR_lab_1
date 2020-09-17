import requests
import time
import concurrent.futures

base_url = 'http://localhost:5000'
base_request = requests.get(base_url + '/register').json()
access_token = base_request['access_token']
# r1.json()['link'].values(), base_request['access_token'], executor
r1 = requests.get(base_url + base_request['link'], headers = {'X-Access-Token': base_request['access_token']})
def make_requests(routes, e):
    for route in routes:
        req = requests.get(base_url + route, headers = {'X-Access-Token': access_token})
        print(req.json())
        print('\n')
        if 'link' in req.json():
            e.submit(make_requests, req.json()['link'].values(), access_token, e)
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda p: make_requests(*p), r1.json()['link'].values(), executor)
        time.sleep(20)

if __name__ == "__main__":
    main()