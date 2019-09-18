import scrapy
import re
from scrapy.loader import ItemLoader
from wordcloud.items import WordcloudItem


class GenericSpider(scrapy.Spider):
    name = "generic"

    def start_requests(self):
        # index = 0
        # for line in siteDataList:
        line = getattr(self, 'site_url', None)
        if line is not None:
            siteData = line.split(',')
            if len(siteData) > 1:
                isScrapped = int(siteData[0])
                scrapLevel = int(siteData[1])
                url = siteData[2]
                if isScrapped == 0:
                    request = scrapy.Request(url, callback=self.parseRootUrl)
                    request.cb_kwargs['root'] = self.extractBaseUrl(url)
                    request.cb_kwargs['projectRoot'] = self.extractProjectRoot(
                        url)
                    request.cb_kwargs['level'] = scrapLevel
                    request.cb_kwargs['current_level'] = 0

                    yield request
            # index += 1

    def extractBaseUrl(self, url):
        fragments = url.split('/')
        return fragments[0] + "//" + fragments[2]

    def extractProjectRoot(self, url):
        fragments = url.split('/')
        return fragments[0] + "//" + fragments[2] + "/" + fragments[3]

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
