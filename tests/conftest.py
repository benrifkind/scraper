import pytest

from scraper.storage.db.db import DB_URL, _engine, init_db
from sqlalchemy_utils import drop_database


@pytest.fixture(autouse=True, scope="function")
def session():
    # Double check that in testing environment
    assert "test" in DB_URL, "Set the environment variable SCRAPER_ENV=test"

    # Hack to reset connections to the DB since the DB has been dropped and so the
    # existing connections were terminated. This is to handle this error:
    # sqlalchemy.exc.OperationalError: (psycopg2.errors.AdminShutdown) terminating connection
    # due to administrator command server closed the connection unexpectedly
    # This probably means the server terminated abnormally before or while processing the request."
    # See https://docs.sqlalchemy.org/en/13/core/connections.html#engine-disposal
    _engine.dispose()

    init_db(db_url=DB_URL, drop=True)
    yield

    assert "test" in DB_URL
    drop_database(url=DB_URL)
