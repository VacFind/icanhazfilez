#parse.py
import wget
from pathlib import Path
import requests
import argparse
from bs4 import BeautifulSoup, SoupStrainer

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("link_filter")
#dry run

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
    if a['href'].endswith(args.link_filter):
        links.append(base_url + a['href'])

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