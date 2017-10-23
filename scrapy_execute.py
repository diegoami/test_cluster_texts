
from technews_nlp_aggregator.scraping.google_search_wrapper import Command, create_google_service, Iterator
from technews_nlp_aggregator.scraping.technews_retriever import Raw_Retriever
from technews_nlp_aggregator.scraping.othersites.arstechnica.spiders import JobsSpider
from technews_nlp_aggregator.scraping.othersites.arstechnica import ArstechnicaPipeline

import yaml
import scrapy
from scrapy.crawler import CrawlerProcess

config = yaml.safe_load(open('config.yml'))
pipeline = ArstechnicaPipeline()
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.othersites.arstechnica import settings

crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)

process.crawl(JobsSpider)
process.start()


