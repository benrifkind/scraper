from scraper.parser.craigslist.link_parser import CraigslistLinkParser
from scraper.parser.craigslist.listing_parser import CraigslistListingParser


def test_craigslist_listing_parser():
    with open("tests/resources/craigslist_listing.html") as f:
        html = f.read()
    parser = CraigslistListingParser(html=html)

    assert (
        parser.serialize
        == """{"address": null, "area": "toronto", "attrs": ["1BR / 1Ba", "apartment", "attached garage", "available may 9", "dogs are OK - wooof", "furnished", "no smoking", "w/d in unit", "wheelchair accessible"], "category": "vacation rentals", "geocode": {"accuracy": "5", "latitude": "43.670634", "longitude": "-79.376307"}, "posting_body": "\\n\\nModern and elegant 1 bedroom in prime Downtown Toronto location. \\n\\n\\nYour Fully Furnished & Equipped apartment includes:\\n\\nHigh Speed Unlimited Internet\\nRogers Premier Cable TV with 170+ channels\\n43\\" 4K Smart TV\\n", "price": "$3870", "sub_area": "city of toronto", "title": "FURNISHED 1 bedroom condo downtown Toronto. BRAND NEW! must see."}"""
    )


def test_craigslist_link_parser():
    with open("tests/resources/craigslist_listing_links.html") as f:
        html = f.read()

    parser = CraigslistLinkParser(html=html)
    assert parser.next_url
    assert len(parser.links) == 120
