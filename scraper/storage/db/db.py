import os
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Index, String, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

DB_NAME = "scraper"
ENV = os.getenv("SCRAPER_ENV", "development")
DB_URL_DEVELOPMENT = f"postgresql://postgres:@db/scraper_{ENV}"
DB_URL = os.getenv("DB_URL", DB_URL_DEVELOPMENT)

_engine = create_engine(DB_URL)
Base = declarative_base(bind=_engine)


class Url(Base):
    __tablename__ = "urls"
    __table_args__ = (Index("idx_urls_url", "url"),)

    url = Column(String, unique=True, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    visited_at = Column(DateTime)
    blob = Column(JSONB)


class Db:
    _session: session.Session = sessionmaker(bind=_engine, autocommit=True)()

    @classmethod
    def filter(cls, urls: List[str]):
        existing_urls = set(
            u.url for u in cls._session.query(Url).filter(Url.url.in_(urls)).all()
        )
        new_urls = [url for url in urls if url not in existing_urls]
        return new_urls

    @classmethod
    def add(cls, url: str, blob: str):
        mappings = [{"url": url, "blob": blob, "visited_at": datetime.utcnow()}]
        cls._session.bulk_insert_mappings(mapper=Url, mappings=mappings)

    @classmethod
    def get(cls, url: str) -> Optional[str]:
        record = cls._session.query(Url).filter(Url.url == url).first()
        if record is not None:
            return record.blob


def init_db(db_url: str, drop: bool) -> None:
    # This exist as safeguard to avoid running on production or staging
    # assert "localhost" in db_url
    if database_exists(db_url):
        if not drop:
            ask = input(
                f"{db_url} already exists. Do you want to drop it (y/N)?"
            ).lower()
            if not (ask == "y"):
                print("Exiting")
                return
        drop_database(db_url)

    create_database(db_url)
    Base.metadata.create_all()
