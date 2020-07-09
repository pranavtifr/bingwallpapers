#!/usr/bin/python
"""Download bing wallpapers from all regions."""

import re
import sys
import urllib
import itertools

if sys.version_info[0] < 3:
    print("SERIOUSLY, STOP USING PYTHON2.")
    import urllib2

else:
    import requests  # noqa
from subprocess import call
import pickle

# Latest Homepage xml Url

# Fucntion For Extracting Image Url and Image Details From xml
downloaded = []
try:
    with open("outfile", "rb") as fp:
        downloaded = pickle.load(fp)
except FileNotFoundError:
    pass


def get_image_details(xml):
    """Get image url."""
    # Url and Details Pattern
    image_url_pattern = "<url>(.*?)</url>.+<copyright>(.*?)</copyright>"

    # search patterns
    (img_url, img_detail) = re.search(image_url_pattern, xml).groups(1)

    # Complete Url
    bing = "http://www.bing.com" + img_url
    return (bing, img_url)


# Function for Downloading Image
def download_image(url):
    """Download the image."""
    filename = re.findall("OHR.[\\w-]*.jpg", url)
    try:
        print(filename[0][4:])
    except IndexError:
        print(filename, url)
        exit()
    call(["wget", "-nc", "-q", "-O", filename[0][4:], url])


# Main Function
def dostuff(url):
    """DO STUFF."""
    try:
        if sys.version_info[0] < 3:
            f = urllib2.urlopen(url)
        else:
            f = urllib.request.urlopen(url)
    except urllib.error.URLError:
        print("Error: Maybe Invalid ID")
        exit(0)
        # Extract Image Url From Xml
    (img_url, img_detail) = get_image_details(f.read().decode())
    # Download Image
    name = re.findall("\\w*_", img_detail)
    lol = name[0][: name[0].find("_")]
    print(downloaded, lol)
    if lol not in downloaded:
        print("downloading")
        download_image(img_url)
        downloaded.append(lol)
    return


# Main Function Trigger
if __name__ == "__main__":
    for mkt, idx in itertools.product(
        [
            "es-AR",
            "en-AU",
            "de-AT",
            "nl-BE",
            "fr-BE",
            "pt-BR",
            "en-CA",
            "fr-CA",
            "fr-FR",
            "de-DE",
            "zh-HK",
            "en-IN",
            "en-ID",
            "it-it",
            "ja-JP",
            "ko-KR",
            "en-MY",
            "es-MX",
            "nl-NL",
            "nb-NO",
            "zh-CN",
            "pl-PL",
            "ru-RU",
            "ar-SA",
            "en-ZA",
            "en-ES",
            "sv-SE",
            "fr-CH",
            "de-CH",
            "zh-TW",
            "tr-TR",
            "en-GB",
            "en-US",
            "es-US",
        ],
        range(10),
    ):
        print(idx, mkt)
        url = (
            "http://www.bing.com/HPImageArchive.aspx?format=xml&idx="
            + str(idx)
            + "&n=1"
            + "&mkt="
            + mkt
        )
        dostuff(url)

    N = 30
    """
    if len(downloaded) > N:
        print("Deleting Old ones")
        for k in downloaded[:len(downloaded)-N]:
            print(k)
            command = 'rm -v $(ls | grep '+k+')'
            call([command],shell = True)
        downloaded = downloaded[-N:]
    """
    with open("outfile", "wb") as fp:
        pickle.dump(downloaded, fp)
