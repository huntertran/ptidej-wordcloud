from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from nlp.NlpProcessing import process
from model.Site import Site
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

        # Crawling
        if not site.IsCrawled:
            # TODO: edit here to stop re-scraping a site on different run
            siteDataList[index].IsCrawled = True
            yield runner.crawl(crawler, siteUrl=site.SiteUrl, crawlDepthLevel=site.CrawlDepthLevel)
        index += 1

    with open(filePath, 'w') as dataFile:
        json.dump(siteDataList, dataFile, default=Site.encode_Site, indent=4)

    reactor.stop()

def nlp():
    filePath = './ptidejWordcloud/sitelist.json'

    with open(filePath, 'r') as dataFile:
        siteDataList = json.load(dataFile, object_hook=Site.decode_Site)

    index = 0
    for site in siteDataList:
        # NLP Processing
        if not site.IsWordcloudGenerated:
            process(site.SiteUrl)
            siteDataList[index].IsWordcloudGenerated = True
        index += 1

    with open(filePath, 'w') as dataFile:
        json.dump(siteDataList, dataFile, default=Site.encode_Site, indent=4)

    reactor.stop()

crawl()
reactor.run()
nlp()
reactor.run()