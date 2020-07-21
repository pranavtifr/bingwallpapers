#! /usr/bin/env python
"""Download bing wallpapers from all regions."""

import re
import urllib
from datetime import date
import requests  # noqa
from subprocess import call
import pickle

# Latest Homepage xml Url

# Fucntion For Extracting Image Url and Image Details From xml
downloaded = []
try:
    with open("unsplash_outfile", "rb") as fp:
        downloaded = pickle.load(fp)
except FileNotFoundError:
    pass


# Function for Downloading Image
def download_image(url, filename):
    """Download the image."""
    print(f"{filename} on {date.today()}")
    call(["wget", "-q", "-U", "firefox", "-O", f"Unsplash_{filename}.jpg", url])


# Main Function
def dostuff(url):
    """DO STUFF."""
    try:
        f = urllib.request.urlopen(url)
    except urllib.error.URLError:
        print("Error: Maybe Invalid ID")
        exit(0)
        # Extract Image Url From Xml
    webpage = f.read().decode()
    # Download Image
    name = re.findall('href="/photos/[\\w_]*"', webpage)
    for objects in name:
        lol = objects[14:-1]
        if lol not in downloaded:
            img_url = f"https://unsplash.com/photos/{lol}/download?force=true"
            download_image(img_url, lol)
            downloaded.append(lol)
    return


# Main Function Trigger
if __name__ == "__main__":
    url = (
        "https://unsplash.com/s/photos/wallpapers?order_by=latest&orientation=landscape"
    )
    dostuff(url)

    with open("unsplash_outfile", "wb") as fp:
        pickle.dump(downloaded, fp)
