from typing import List, Optional

from cached_property import cached_property
from scraper.parser.core import LinkParser


class CraigslistLinkParser(LinkParser):
    @cached_property
    def links(self) -> List[str]:
        """Extract the links from a page"""
        a_tags = self.bs.find_all("a")
        links = [
            a
            for a in a_tags
            if a.get("class") is not None and "result-title" in a.get("class")
        ]

        return [link.get("href") for link in links]

    @cached_property
    def next_url(self) -> Optional[str]:
        """Extracts the next url which will contain more links to listings"""
        link = self.bs.head.find("link", rel="next")
        if link is not None:
            return link.get("href")
