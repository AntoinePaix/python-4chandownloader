#!/usr/bin/python3
# Coding: utf8

import requests
import argparse
import re
import os
from bs4 import BeautifulSoup

# Author : Antoine Paix
# Date : 11/03/2020

parser = argparse.ArgumentParser(description='Download media files from a 4chan thread')
parser.add_argument('-u', '--url', type=str, required=True, help='4chan thread url')
args = parser.parse_args()

url = args.url

def create_directory():
    """Create folder if it does not exist."""
    foldername = re.split('/+', url)[-1]
    if os.path.isdir(foldername):
        return foldername
    else:
        os.mkdir(foldername)
        return foldername


def get_media_links(url):
    """Return all media links in 4chan thread."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()

    for link in soup.find_all('a'):
        link = link.get('href')
        if link.startswith('//i.4cdn.org/'):
            link = 'https:' + link
            links.add(link)
    
    return links

def download_file(url):
    """download media file with requests module"""
    filename = re.split('/+', url)[-1]
    filepath = os.path.join(create_directory(), filename)

    # if file already exists, print message
    if os.path.isfile(filepath):
        print(filename, 'already downloaded')
    
    else:
        with open(filepath, 'wb') as handler:
            content = requests.get(url).content
            try:
                handler.write(content)
                print(filename, 'downloaded')
            except IOError:
                print('Impossible to write the file')

# MAIN PROGRAM
if __name__ == '__main__':

    for link in get_media_links(url):
        download_file(link)
