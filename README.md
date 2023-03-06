# scraper-technical-assignment 

## Docker

	$ docker build --tag cdbscraper .

	$ cat websites.txt | docker run -i cdbscraper


## Python

    $ cat websites.txt | python -m cdbscraper

## Requirements

* [Framework Scrapy](cdbscraper/scrapy.cfg);
* [Dynamic Scraper (Uses headless navigation)](cdbscraper/cdbscraper/settings.py#L112);
* [stdin](cdbscraper/__main__.py#L17) - [stdout](cdbscraper/cdbscraper/spiders/cdbspider.py#L117) - [stderr](cdbscraper/cdbscraper/settings.py#L20);
* [Coding header](cdbscraper/cdbscraper/spiders/cdbspider.py#L1);
* [Python3](Dockerfile#L1);
* [Dockerfile](Dockerfile);
* Pep8 guidelines (Formatted with ```$ black --line-length 79 *.py```);
* [Identify unique phone numbers](cdbscraper/cdbscraper/spiders/cdbspider.py#L96);
* [Code concurrent](cdbscraper/cdbscraper/settings.py#L38).