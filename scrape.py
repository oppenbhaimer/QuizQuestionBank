from bs4 import BeautifulSoup
import os
import requests
import json
import sys
from tqdm.auto import tqdm

def parse_data(fname):
    data = {}
    with open(fname, 'r') as file:
        line = file.readline().strip()
        tokens = [a.split('=', 1) for a in line.split("; ")]
        for (a, b) in tokens:
            data[a] = b 
    return data

# html_doc = open(sys.argv[1])
usernames = json.load(open('scrape/usernames.json', 'r'))
root = "https://www.slideshare.net"
formdata = json.load(open('scrape/authtoken.json', 'r'))
cookies = json.load(open('scrape/cookies.json', 'r'))

def download(name: str, url, dest_dir):
    name = name.strip().replace(' ', '_')+'.pdf'
    response = requests.post(root+url, data=formdata, cookies=cookies)

    if response.status_code != 200:
        print(f'An error occured while downloading {url}')
        return

    tgt = json.loads(response.text)
    if tgt['success']:
        download = requests.get(tgt['url'])
        with open(dest_dir+'/'+name, 'wb') as outfile:
            outfile.write(download.content)

def dummy_download(name, url):
    name = name.replace(' ', '_')+'.pdf'
    # print(f'Downloading {name} from {root}{url}')

def user_download(username, dummy=False):
    doc = requests.get(root+'/'+username).text
    soup = BeautifulSoup(doc, 'html.parser')

    # Extract all divs with class edit-settings-tray
    divs = soup.find_all('div', class_='slideshow-card')

    urls = []

    # Extract the data-download parameter inside the button in the div
    for div in divs:
        button = div.find('button')
        title = div.find_all('div', class_='thumb')[0].get('title')
        if button:
            data_download = button.get('data-download')
            urls.append((title, data_download))

    print(f'Downloading {username}')
    try:
        os.mkdir(f'raw/{username}')
    except FileExistsError:
        pass
    for (name, url) in tqdm(urls):
        if dummy:
            dummy_download(name, url)
        else:
            download(name, url, f'raw/{username}')

for username in usernames:
    user_download(username, dummy=False)
