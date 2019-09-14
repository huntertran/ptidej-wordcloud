import scrapy
from scrapy.loader import ItemLoader
from wordcloud.items import WordcloudItem


class PahoSpider(scrapy.Spider):
    name = "paho"
    urls = []

    def start_requests(self):
        filePath = './wordcloud/spiders/sitelist.txt'
        with open(filePath, 'r') as dataFile:
            siteDataList = dataFile.readlines()

        index = 0
        for line in siteDataList:
            siteData = line.split(',')
            if len(siteData) > 1:
                isScrapped = siteData[0]
                scrapLevel = int(siteData[1])
                url = siteData[2]
                self.urls.append(url)
                if isScrapped == 0:
                    # TODO: edit here to stop re-scraping a site on different run
                    siteDataList[index] = '0,' + scrapLevel + ',' + url + '\n'
    
                    request = scrapy.Request(url, callback=self.parseRootUrl)
                    request.cb_kwargs['root'] = self.extractBaseUrl(url)
                    request.cb_kwargs['projectRoot'] = self.extractProjectRoot(url)
                    request.cb_kwargs['level'] = scrapLevel
                    request.cb_kwargs['current_level'] = 0
    
                    yield request
            index += 1

        with open(filePath, 'w') as dataFile:
            dataFile.writelines(siteDataList)

    def extractBaseUrl(self, url):
        fragments = url.split('/')
        return fragments[0] + "//" + fragments[2]

    def extractProjectRoot(self, url):
        fragments = url.split('/')
        return fragments[0] + "//" + fragments[2] + "/" + fragments[3]

    def parseRootUrl(self, response, root, projectRoot, level, current_level):

        # response for base url
        # self.parseUrl(response)

        urls = response.selector.xpath("//a/@href").getall()

        for url in urls:
            if url.startswith('#') == False:
                urlToScrap = self.buildUrl(root, url)
                if root in urlToScrap:
                    request = self.buildRequest(
                        root,
                        projectRoot,
                        urlToScrap,
                        level,
                        current_level)

                    yield request

    def buildRequest(self, root, projectRoot, url, level, currentLevel):
        if level == currentLevel:
            request = scrapy.Request(url, callback=self.parseUrl)
            request.cb_kwargs['projectRoot'] = projectRoot
        else:
            request = scrapy.Request(url, callback=self.parseRootUrl)
            request.cb_kwargs['root'] = root
            request.cb_kwargs['projectRoot'] = projectRoot
            request.cb_kwargs['level'] = level
            request.cb_kwargs['current_level'] = currentLevel + 1
        return request

    def buildUrl(self, root, url):
        if url.startswith('http'):
            return url
        else:
            return root + url

    def cleanText(self, text):
        text = text.strip()
        text = text.strip('\r').strip('\n')
        return text

    def parseUrl(self, response, projectRoot):
        # loader = ItemLoader(item=WordcloudItem(), response=response)

        # loader.add_xpath('text', '//text()')
        # loader.add_value('link', response.url)
        # return loader.load_item()

        page = response.url
        texts = response.xpath('//text()').getall()
        for text in texts:
            text = self.cleanText(text)
            if len(text) != 0:
                yield {
                    "projectRoot": projectRoot,
                    "l": page,
                    "t": text
                }
