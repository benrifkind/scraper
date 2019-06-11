import time
from typing import List, Optional, Type

import attr
import requests

from scraper.parser.core import LinkParser, ListingParser
from scraper.parser.craigslist.link_parser import CraigslistLinkParser
from scraper.parser.craigslist.listing_parser import CraigslistListingParser
from scraper.storage.db.db import Db

DELAY = 5


@attr.s
class Scraper:

    start_url: str = attr.ib()
    link_parser: Type[LinkParser] = attr.ib()
    listing_parser: Type[ListingParser] = attr.ib()

    def run(self):
        """Adds the data from all the listing pages into the database table.
        Starts at a url with links to listings
            - visits each link on the page and adds its content to the database
            - if there is a link to another page with links iterates forward. Otherwise exits.
        """
        urls = self.get_urls()
        unvisited_urls = Db.filter(urls)
        print(f"Downloading {len(unvisited_urls)}/{len(urls)} urls")
        for url in unvisited_urls:
            print(f"Downloading url: {url}")
            blob = self.visit(url=url)
            if blob is not None:
                Db.add(url=url, blob=blob)
            time.sleep(DELAY)

    def get_urls(self) -> List[str]:
        url = self.start_url
        urls = []
        while True:
            time.sleep(DELAY)
            response = requests.get(url)
            response.raise_for_status()

            parser = self.link_parser(html=response.text)

            new_urls = parser.links
            urls += new_urls
            print(f"Found {len(new_urls)} urls for a total of {len(urls)} urls")

            next_link = parser.next_url
            if next_link is None:
                print(f"No more urls to download")
                break
            url = next_link

        return urls

    def visit(self, url: str) -> Optional[str]:
        """
        Visits a link to a listing and returns the parsed html as json
        """
        response = requests.get(url)
        # TODO(ben): handle error instead of ignoring. Or add functionality to retry
        if response.status_code != 200:
            print(f"Unable to download url: {url}")
            return

        return self.listing_parser(html=response.text).serialize


if __name__ == "__main__":
    toronto_apartments_url = "https://toronto.craigslist.org/search/hhh"
    scraper = Scraper(
        start_url=toronto_apartments_url,
        link_parser=CraigslistLinkParser,
        listing_parser=CraigslistListingParser,
    )
    scraper.run()
