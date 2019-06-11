import json
from typing import Dict, List, Optional

import bs4

from cached_property import cached_property
from scraper.parser.core import ListingParser


class CraigslistListingParser(ListingParser):
    @cached_property
    def posting_title(self) -> Optional[bs4.element.Tag]:
        return self.bs.find("h2", class_="postingtitle")

    @cached_property
    def crumbs(self) -> Optional[bs4.element.Tag]:
        return self.bs.find("ul", class_="breadcrumbs")

    @cached_property
    def map_and_attrs(self) -> Optional[bs4.element.Tag]:
        return self.bs.find("div", class_="mapAndAttrs")

    @cached_property
    def posting_body(self) -> bs4.element.Tag:
        body = self.bs.find("section", id="postingbody")
        if body:
            body.div.extract()  # Removes unwanted <div/>
            return body.text

    @property
    def area(self) -> Optional[str]:
        area = self.crumbs.find("li", class_="area")
        return area.a.text if area.a else None

    @property
    def sub_area(self) -> str:
        area = self.crumbs.find("li", class_="subarea")
        return area.a.text if area.a else None

    @property
    def category(self) -> str:
        cat = self.crumbs.find("li", class_="crumb category")
        return cat.a.text if cat.a else None

    @property
    def price(self) -> str:
        p = self.posting_title.find("span", class_="price")
        return p.text if p else None

    @property
    def title(self) -> str:
        t = self.posting_title.find("span", id="titletextonly")
        return t.text if t else None

    @property
    def attrs(self) -> List[str]:
        # A quick look seems to suggest that the attributes of the post are separated into two <p> tags
        ps = self.map_and_attrs.find_all("p", class_="attrgroup")
        if ps:
            return sorted([s.text for p in ps for s in p.find_all("span")])

    @property
    def address(self) -> Optional[str]:
        addr = self.map_and_attrs.find("div", class_="mapaddress")
        if addr:
            return addr.text

    @property
    def geocode(self) -> Dict[str, str]:
        map_data = self.map_and_attrs.find("div", id="map")
        if map_data is None:
            return {}

        return {
            "accuracy": map_data.get("data-accuracy"),
            "latitude": map_data.get("data-latitude"),
            "longitude": map_data.get("data-longitude"),
        }

    @cached_property
    def serialize(self) -> str:
        properties = [
            "address",
            "area",
            "attrs",
            "category",
            "geocode",
            "posting_body",
            "price",
            "sub_area",
            "title",
        ]
        return json.dumps({k: getattr(self, k) for k in properties})
