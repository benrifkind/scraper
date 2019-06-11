from typing import List, Optional

import bs4

from cached_property import cached_property


class LinkParser:
    def __init__(self, html: str):
        self.bs = bs4.BeautifulSoup(html, features="html.parser")

    @cached_property
    def links(self) -> List[str]:
        raise NotImplementedError()

    @cached_property
    def next_url(self) -> Optional[str]:
        raise NotImplementedError()


class ListingParser:
    def __init__(self, html: str):
        self.bs = bs4.BeautifulSoup(html, features="html.parser")

    @cached_property
    def serialize(self) -> str:
        "This defines how the data from the html page is extracted"
        raise NotImplementedError()
