#parse.py
import wget
from pathlib import Path
import requests
import argparse
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
#dry run
parser.add_argument("url", help='The URL to search for links')
parser.add_argument("link_filter", help='the file extension for the files you are looking for')
parser.add_argument("--cookiefile", type=str, help='the path to a text file containing cookies to use')

args = parser.parse_args()

#get HTML page
page = requests.get(args.url)

only_a_tags = SoupStrainer("a")

#check if downloading page was successful
soup = BeautifulSoup(page.text, "html.parser", parse_only=only_a_tags)


links = []

def get_base_url(url):
    last_slash = url.rfind('/')
    return url[:last_slash + 1]

def is_external_link(link):
    return not link.startswith(("http", "www"))

#strip ./ from the front etc
# def cleanup_link():


base_url = get_base_url(args.url)
print(base_url)

#parse and filter links
for a in soup.find_all('a', href=True):
    if urlparse(a['href']).path.endswith(args.link_filter):
        if is_external_link(a['href']):
            links.append(base_url + a['href'])
        else:
            links.append(a['href'])

print(links)

for link in links:
    file_name = link.split("/")[-1]

    if not Path(file_name).is_file():
        try:
            wget.download(link)
        except Exception as e:
            print(link + ": failed with error")
            print(e)
    else:
        print(file_name + ": file already exists on disk")