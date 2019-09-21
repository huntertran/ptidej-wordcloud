import scrapy
import re
from scrapy.loader import ItemLoader
from ptidejWordcloud.items import WordcloudItem


class GenericSpider(scrapy.Spider):
    name = "generic"

    def start_requests(self):
        siteUrl = getattr(self, 'siteUrl', None)
        crawlDepthLevel = getattr(self, 'crawlDepthLevel', 0)

        request = scrapy.Request(siteUrl, callback=self.parseRootUrl)
        request.cb_kwargs['root'] = self.extractBaseUrl(siteUrl)
        request.cb_kwargs['projectRoot'] = self.extractProjectRoot(siteUrl)
        request.cb_kwargs['level'] = crawlDepthLevel
        request.cb_kwargs['current_level'] = 0

        yield request

    def extractBaseUrl(self, url):
        fragments = url.split('/')
        return fragments[0] + "//" + fragments[2]

    def extractProjectRoot(self, url):
        fragments = url.split('/')
        root = fragments[0] + "//" + fragments[2]
        
        if len(fragments) == 3:
            return root
        else:
            return root + '/' + fragments[3]

    def parseRootUrl(self, response, root, projectRoot, level, current_level):
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

        for item in self.parseUrl(response, projectRoot):
            yield item

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
        # remove all trailing whitespaces
        text = text.strip()
        # remove all redundant spaces
        text = re.sub(r'\s+', ' ', text)
        # remove newline chars
        text = text.strip('\r').strip('\n')

        return text

    def parseUrl(self, response, projectRoot):
        page = response.url
        texts = response.xpath('//text()[not(ancestor::pre)]').getall()
        for text in texts:
            text = self.cleanText(text)
            if len(text) != 0:
                yield {
                    # "projectRoot": projectRoot,
                    "l": page,
                    "t": text
                }
