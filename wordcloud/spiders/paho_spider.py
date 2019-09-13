import scrapy


class PahoSpider(scrapy.Spider):
    name = "paho"
    baseUrl = ""

    def extractBaseUrl(self, url):
        fragments = url.split('/')
        self.baseUrl = fragments[0] + "//" + fragments[2]

    def start_requests(self):
        urls = [
            'https://www.eclipse.org/paho/',
        ]
        for url in urls:
            self.extractBaseUrl(url)
            yield scrapy.Request(url=url, callback=self.parseUrls)

    def parseUrls(self, response):
        urls = response.selector.xpath("//a/@href").getall()

        for url in urls:
            if url.startswith('#') == False:
                if url.startswith('http'):
                    yield scrapy.Request(url, callback=self.parseUrl)
                else:
                    yield scrapy.Request(url=self.baseUrl + url, callback=self.parseUrl)

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
