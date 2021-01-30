#parse.py
from pathlib import Path
import requests
import argparse
import logging
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
import http.cookiejar 
import re, os
from util.handlers import binary_downloader

parser = argparse.ArgumentParser()
parser.add_argument("url", help='The URL to search for links')
parser.add_argument("link_filter", help='the file extension for the files you are looking for')
parser.add_argument("--cookiefile", type=str, help='the path to a text file containing cookies to use')
parser.add_argument("-v", "--verbose", action='store_true', help='output more information')
parser.add_argument("-n", "--dry-run", action='store_true', help='run the program without actually making any web requests')


args = parser.parse_args()

logger = logging.getLogger(__name__)

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
logger.debug('base url: %s', base_url)

#parse and filter links
for a in soup.find_all('a', href=True):
    if urlparse(a['href']).path.endswith(args.link_filter):
        if is_external_link(a['href']):
            links.append(base_url + a['href'])
        else:
            links.append(a['href'])

logger.debug('links: %s', links)

cj = None
if args.cookiefile is not None:
    cj = http.cookiejar.MozillaCookieJar(args.cookiefile)
    cj.load()


for link in links:

    r= requests.get(link, cookies=cj, stream = True)
    try:
        binary_downloader(r, link)
    except KeyError:
        print("KeyError")
        continue
