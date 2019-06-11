from scraper.storage.db.db import Db, Url


def test_filter():
    Db._session.add_all([Url(url=u) for u in list("123")])
    assert sorted(Db.filter(list("1243"))) == ["4"]


def test_add():
    Db.add(url="2", blob="blob")

    assert Db.get(url="1") is None
    assert Db.get(url="2") == "blob"
