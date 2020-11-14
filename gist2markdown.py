#!/usr/bin/env python

import re
import argparse
import requests

def main():
    args = parse_args()

    gist_id = find_id(args.url, args.follow_redirects)

    if args.verbose:
        print(f"Found gist ID {gist_id}")
    gist_api_adaptor = GistAPIAdaptor(gist_id)
    gist_api_adaptor.fetch()
    file_types = gist_api_adaptor.get_file_langs()
    raw_urls =  gist_api_adaptor.get_raw_urls()
    for i in range(len(raw_urls)):
        output_markdown(file_types[i], raw_urls[i])


def parse_args():
    parser = argparse.ArgumentParser(description="Prints markdown based on some gist url.")
    parser.add_argument("-u", 
            "--url", 
            required=True,
            type=str, 
            help="The gist URL to pull from.")
    parser.add_argument("-d", 
            "--follow-redirects", 
            action="store_true",
            help="Follow redirects when pulling URL. Useful for sites that redirect to github, but place the URL under their own domain, like Medium.")
    parser.add_argument("-v", 
            "--verbose", 
            default=False,
            action="store_true",
            help="Verbose output.")

    return parser.parse_args()

def find_id(url, follow_redirects):

    if "gist.github" in url:
        gist_id = search_for_gist_id(url)

        if gist_id:
            return gist_id

    resp = requests.get(url, allow_redirects=follow_redirects)
    gist_id = search_for_gist_id(resp.text)

    if not gist_id:
        raise Exception(f"Unable to find gist ID in url: {url}\n Are you sure the URL is correct?")

    return gist_id

def output_markdown(file_type, raw_url):
    print(f"```{file_type}")
    print(requests.get(raw_url).text)
    print(f"```")

def search_for_gist_id(url):
    # Gist ID is 32 characters e.g. f0cba2cdad0afa4ca50c293256bf7b79
    # This could break in cases where a 32 character word satisfying the below regex is present, but, 
    # for most urls, it should be fine.
    result = re.search("[0-9a-zA-Z]{32}", url)
    if result:
        return result.group(0)

    return ""

class GistAPIAdaptor:
    """ Gists have an API I'm leveraging here to gain information about the gist in question:
        https://developer.github.com/v3/gists/

        Intended for a single gist.
    """

    def __init__(self, gist_id):
        self.gist_id = gist_id
        self.api_endpoint = "https://api.github.com/gists"
        self._data = {}

    def fetch(self):
        """ Pull general data about this gist"""
        data = requests.get(f"{self.api_endpoint}/{self.gist_id}")
        if not data:
            raise Exception(f"Was unable to find gist with id: {self.gist_id}")

        self._data = data.json()
    
    def get_file_langs(self):
        """ Pull the filetype from gist data """
        langs = []
        for filename in self._data['files'].keys():
            langs.append(self._data['files'][filename]['language'])

        return langs

    def get_raw_urls(self):
        urls = []
        for filename in self._data['files'].keys():
            urls.append(self._data['files'][filename]['raw_url'])

        return urls


if __name__ == "__main__":
    main()
