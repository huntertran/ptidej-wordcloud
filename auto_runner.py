from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from ptidejWordcloud.spiders import generic_spider
from nlp.NlpProcessing import process

settings = get_project_settings()
configure_logging(settings=settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():

    crawler = runner.spider_loader.list()[0]

    filePath = './ptidejWordcloud/sitelist.txt'

    with open(filePath, 'r') as dataFile:
        siteDataList = dataFile.readlines()

    index = 0
    for line in siteDataList:
        line = line.strip('\n').strip('\r')
        siteData = line.split(',')
        if len(siteData) > 1:
            isScrapped = int(siteData[0])
            scrapLevel = int(siteData[1])
            url = siteData[2]
            if isScrapped == 0:
                # TODO: edit here to stop re-scraping a site on different run
                siteDataList[index] = '1,' + str(scrapLevel) + ',' + url + '\n'
                yield runner.crawl(crawler, site_url=line)
        index += 1
        with open(filePath, 'w') as dataFile:
            dataFile.writelines(siteDataList)

        # NLP Processing
        process(url)

    reactor.stop()

# def nlp():
#     NlpProcessing.combineStopwords()
#     quit()


crawl()
# nlp()
reactor.run()
