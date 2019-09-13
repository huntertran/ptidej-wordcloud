import scrapy


class PahoSpider(scrapy.Spider):
    name = "paho"
    baseUrl = ""

    def extractBaseUrl(self, url):
        fragments = url.split('/')
        return fragments[0] + "//" + fragments[2]

    def start_requests(self):
        filePath = './wordcloud/spiders/sitelist.txt'
        with open(filePath, 'r') as dataFile:
            siteDataList = dataFile.readlines()
        
        index = 0
        for line in siteDataList:
            isScrapped = line.split(',')[0]
            url = line.split(',')[1]
            if isScrapped == '0':
                siteDataList[index] = '1,' + url + '\n'
                baseUrl = self.extractBaseUrl(url)
                request = scrapy.Request(url,callback=self.parseRootUrl)
                request.cb_kwargs['root'] = baseUrl
                yield request
            index += 1
        
        with open(filePath, 'w') as dataFile:
            dataFile.writelines(siteDataList)

    def parseRootUrl(self, response, root):
        urls = response.selector.xpath("//a/@href").getall()

        for url in urls:
            if url.startswith('#') == False:
                if url.startswith('http'):
                    self.log("end")
                    yield scrapy.Request(url, callback=self.parseUrl)
                else:
                    yield scrapy.Request(url=root + url, callback=self.parseUrl)

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
