## Scraper

This is a very simple scraper meant to scrape data from websites like
craigslist, kijiji, viewit.ca  
The scraper works by first getting a list of urls corresponding to listings. 
It then visits each of these urls, scrapes the page, and dumps the data into storage -
in this case a postgresql database.  
There are two types of html pages that need to be parsed. 
One to extract links and one to extract listing data.  
To deal with this, we define two parsers, one for each type of html.
1. `LinkParser`: Parses html that contain links to listings
2. `ListingParser`: Parses html that contains information about a listing

The interface for these parsers are defined in `parser/core.py`

The scraper starts with a url that points to a page containing 
links to listings for a particular category of listing. It
uses the corresponding `LinkParser` to iterate through 
and get all links to listings for that category. 
These links are then used along with the `ListingParser` to extract the listing data which is stored.

Example usage:
```python
from scraper.scrape import Scraper
from scraper.parser.craigslist.link_parser import CraigslistLinkParser
from scraper.parser.craigslist.listing_parser import CraigslistListingParser
url = "https://toronto.craigslist.org/search/hhh"
scraper = Scraper(
    start_url=url,
    link_parser=CraigslistLinkParser,
    listing_parser=CraigslistListingParser,
)
scraper.run()
```
  

## Develop
Development happens through docker containers.  
To run a shell:

```bash
$ make develop   
```
    
This will drop you into a development shell connected to a postgres container. 

The first time you do this you will need to create the development database. 
Do this by running (from inside the development shell):
```bash
$ python scripts/init_db.py
``` 

To scrape from inside the container run:
```bash
$ python scraper.scrape.py
```

The Docker container's directory is synced with the host directory so code
changes will be automatically picked up. 
However, if you need to update the Docker image (eg., due to changing `requirements.txt`),
run (from the host machine):
```bash
docker build -t scraper:latest .
``` 

#### Running tests
Testing happens through docker containers
```bash
make test
```
