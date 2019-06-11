from scraper.storage.db.db import DB_URL, init_db

if __name__ == "__main__":
    init_db(db_url=DB_URL, drop=False)
