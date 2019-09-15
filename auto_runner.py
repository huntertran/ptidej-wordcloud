from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from wordcloud.spiders import generic_spider

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    filePath = './wordcloud/spiders/sitelist.txt'
    with open(filePath, 'r') as dataFile:
        siteDataList = dataFile.readlines()

    index = 0
    for line in siteDataList:
        siteData = line.split(',')
        if len(siteData) > 1:
            isScrapped = int(siteData[0])
            scrapLevel = int(siteData[1])
            url = siteData[2]
            if isScrapped == 0:
                # TODO: edit here to stop re-scraping a site on different run
                siteDataList[index] = '0,' + str(scrapLevel) + ',' + url + '\n'
                yield runner.crawl(generic_spider, site_url=url)
        index += 1
    with open(filePath, 'w') as dataFile:
        dataFile.writelines(siteDataList)
    
    reactor.stop()

crawl()
reactor.run()