import scrapy


class PahoSpider(scrapy.Spider):
    name = "paho"

    def start_requests(self):
        filePath = './wordcloud/spiders/sitelist.txt'
        with open(filePath, 'r') as dataFile:
            siteDataList = dataFile.readlines()
        
        index = 0
        for line in siteDataList:
            siteData = line.split(',')
            isScrapped = siteData[0]
            scrapLevel = siteData[1]
            url = siteData[2]
            if isScrapped == '0':
                # TODO: edit here to stop re-scraping a site on different run
                siteDataList[index] = '0,' + scrapLevel + ',' + url + '\n'
                baseUrl = self.extractBaseUrl(url)
                request = scrapy.Request(url,callback=self.parseRootUrl)
                request.cb_kwargs['root'] = baseUrl
                # TODO: convert scrapLevel to number
                request.cb_kwargs['level'] = int(scrapLevel)
                request.cb_kwargs['current_level'] = 0
                yield request
            index += 1
        
        with open(filePath, 'w') as dataFile:
            dataFile.writelines(siteDataList)

    def extractBaseUrl(self, url):
        fragments = url.split('/')
        return fragments[0] + "//" + fragments[2]

    def parseRootUrl(self, response, root,level, current_level):
        urls = response.selector.xpath("//a/@href").getall()

        for url in urls:
            if url.startswith('#') == False:
                urlToScrap = self.buildUrl(root, url)

                request = self.buildRequest(root,urlToScrap,level,current_level)

                yield request

    def buildRequest(self,root, url, level, currentLevel):
        if level == currentLevel:
            request = scrapy.Request(url, callback=self.parseUrl)
        else:
            request = scrapy.Request(url, callback=self.parseRootUrl)
            request.cb_kwargs['root'] = root
            request.cb_kwargs['level'] = level
            request.cb_kwargs['current_level'] = currentLevel +1
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

    def parseUrl(self, response):
        page = response.url
        texts = response.xpath('//text()').getall()
        for text in texts:
            text = self.cleanText(text)
            if len(text) != 0:
                yield {
                    'link': page,
                    'text': text
                }
