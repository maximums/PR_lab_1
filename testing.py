import requests
import concurrent.futures

base_url = 'http://localhost:5000'
base_request = requests.get(base_url + '/register').json()
r1 = requests.get(base_url + base_request['link'], headers = {'X-Access-Token': base_request['access_token']})
def make_requests(next_route, access_token, e):
    req = requests.get(base_url + next_route, headers = {'X-Access-Token': access_token})
    print(req.json())
    if 'link' in req.json():
        for lin in req.json()['link'].values():
            e.submit(make_requests, lin, access_token, e)
    return req.json()
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for next_route in r1.json()['link'].values():
            executor.submit(make_requests, next_route, base_request['access_token'],executor)
        

if __name__ == "__main__":
    main()