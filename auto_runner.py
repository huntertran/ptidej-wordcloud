import json
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from nlp.NlpProcessing import process
from model.Site import Site
from nlp.Linker import create_link
from nlp.SentenceAnalyzer import start_analyze
from sigma_helper.convert_data import start_convert


settings = get_project_settings()
configure_logging(settings=settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():

    crawler = runner.spider_loader.list()[0]

    file_path = './data/sitelist.json'

    with open(file_path, 'r') as dataFile:
        site_data_list = json.load(dataFile, object_hook=Site.decode_object)

    index = 0
    for site in site_data_list:

        # Crawling
        if not site.IsCrawled:
            # TODO: edit here to stop re-scraping a site on different run
            site_data_list[index].IsCrawled = True
            yield runner.crawl(crawler, siteUrl=site.SiteUrl, crawlDepthLevel=site.CrawlDepthLevel)
        index += 1

    with open(file_path, 'w') as dataFile:
        json.dump(site_data_list, dataFile, default=Site.encode_object, indent=4)

    if reactor.running:
        reactor.stop()
    else:
        yield runner.crawl(crawler, siteUrl="http://www.msftconnecttest.com/connecttest.txt", crawlDepthLevel=0)
        reactor.stop()


def nlp():
    file_path = './data/sitelist.json'

    with open(file_path, 'r') as dataFile:
        site_data_list = json.load(dataFile, object_hook=Site.decode_object)

    index = 0
    for site in site_data_list:
        # NLP Processing
        if not site.IsWordcloudGenerated:
            process(site.SiteUrl)
            site_data_list[index].IsWordcloudGenerated = True
        index += 1

    with open(file_path, 'w') as dataFile:
        json.dump(site_data_list, dataFile, default=Site.encode_object, indent=4)


crawl()
reactor.run()

# nlp()
# create_link()
# start_analyze()
# start_convert()