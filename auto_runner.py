from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from ptidejWordcloud.spiders import generic_spider
from nlp.NlpProcessing import process
from model.Site import Site
from helpers.ProjectHelper import ProjectHelper
import json

settings = get_project_settings()
configure_logging(settings=settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():

    crawler = runner.spider_loader.list()[0]

    filePath = './ptidejWordcloud/sitelist.json'

    with open(filePath, 'r') as dataFile:
        siteDataList = json.load(dataFile, object_hook=Site.decode_Site)

    index = 0
    for site in siteDataList:
        if not site.IsCrawled:
            # TODO: edit here to stop re-scraping a site on different run
            siteDataList[index].IsCrawled = True
            yield runner.crawl(crawler, site_url=site.SiteUrl)
        index += 1
        with open(filePath, 'w') as dataFile:
            json.dump(siteDataList)

        # NLP Processing
        process(site.SiteUrl)

    reactor.stop()

# def nlp():
#     NlpProcessing.combineStopwords()
#     quit()


crawl()
# nlp()
reactor.run()
