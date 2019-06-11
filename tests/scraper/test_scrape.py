from unittest import mock

from scraper.scrape import Scraper
from scraper.storage.db.db import Db


@mock.patch("scraper.scrape.requests")
@mock.patch("scraper.scrape.DELAY", 0)
def test_scrape(mock_request):
    mock_request.get.return_value.status_code = 200

    link_parser = mock.MagicMock()
    instance = link_parser()
    type(instance).next_url = mock.PropertyMock(side_effect=["http://a.b.com", None])
    type(instance).links = mock.PropertyMock(
        side_effect=[["http://a", "http://b"], ["http://c"]]
    )

    listing_parser = mock.MagicMock()
    instance = listing_parser()
    type(instance).serialize = mock.PropertyMock(
        side_effect=["bloba", "blobb", "blobc"]
    )

    url = "http://this.url.is.unused"
    scraper = Scraper(
        start_url=url, link_parser=link_parser, listing_parser=listing_parser
    )
    scraper.run()
    assert Db.get("http://a") == "bloba"
    assert Db.get("http://b") == "blobb"
    assert Db.get("http://c") == "blobc"
