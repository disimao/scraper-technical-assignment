# scraper-technical-assignment 

## Docker

	$ docker build --tag cdbscraper .

	$ cat websites.txt | docker run -i cdbscraper


## Python

    $ cat websites.txt | python -m cdbscraper

## Requirements

* [Framework Scrapy](cdbscraper/scrapy.cfg);
* Static [Phisical] Scraper (Dynamic Scraper would require headless navigation);
* [stdin](cdbscraper/__main__.py#L16) - [stdout](cdbscraper/cdbscraper/spiders/cdbspider.py#L55) - [stderr](cdbscraper/cdbscraper/settings.py#L20);
* Coding header;
* [Python3](Dockerfile#L1);
* [Dockerfile](Dockerfile);
* Pep8 guidelines;
* [Identify unique phone numbers](cdbscraper/cdbscraper/spiders/cdbspider.py#L52);
* [Code concurrent](cdbscraper/cdbscraper/settings.py#L38).