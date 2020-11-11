import scrapy
import re
from bs4 import BeautifulSoup

from scrapy.loader import ItemLoader
from scrapy.http.response.text import TextResponse
from ptidejWordcloud.items import WordcloudItem
from helpers.ProjectHelper import ProjectHelper


class GenericSpider(scrapy.Spider):
    name = "generic"

    def start_requests(self):
        siteUrl = getattr(self, 'siteUrl', None)
        crawlDepthLevel = int(getattr(self, 'crawlDepthLevel', 0))

        request = scrapy.Request(siteUrl, callback=self.parseRootUrl)
        request.cb_kwargs['root'] = self.extractBaseUrl(siteUrl)
        request.cb_kwargs['projectRoot'] = self.extractProjectRoot(siteUrl)
        request.cb_kwargs['level'] = crawlDepthLevel
        request.cb_kwargs['current_level'] = 0
        request.cb_kwargs['project_name'] = ProjectHelper.getProjectName(
            siteUrl)

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

    def parseRootUrl(self, response, root, projectRoot, level, current_level, project_name):
        urls = response.selector.xpath("//a/@href").getall()

        for url in urls:
            if url.startswith('#') == False:
                urlToScrap = self.buildUrl(root, url)
                # if root in urlToScrap:
                # if root in urlToScrap and project_name in urlToScrap.lower():
                if project_name in urlToScrap.lower():

                    if type(current_level) is tuple:
                        current_level = current_level[0]

                    request = self.buildRequest(
                        root,
                        projectRoot,
                        urlToScrap,
                        level,
                        current_level,
                        project_name)

                    yield request
                else:
                    test = ""

        for item in self.parseUrl(response, projectRoot):
            yield item

    def buildRequest(self, root, projectRoot, url, level, currentLevel, project_name):
        if level == currentLevel:
            request = scrapy.Request(url, callback=self.parseUrl)
            request.cb_kwargs['projectRoot'] = projectRoot
        else:
            request = scrapy.Request(url, callback=self.parseRootUrl)
            request.cb_kwargs['root'] = root
            request.cb_kwargs['projectRoot'] = projectRoot
            request.cb_kwargs['level'] = level
            request.cb_kwargs['current_level'] = currentLevel + 1,
            request.cb_kwargs['project_name'] = project_name
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

    def isLineMatchCode(self, line):
        matchCode = re.search(r'\S+\s?\{(.+)\}', line)
        if matchCode:
            return True
        else:
            return False

    def parseUrl(self, response, projectRoot):
        page = response.url
        if 'text' in response.headers['Content-Type'].decode('utf-8'):
            # # soup = BeautifulSoup(response.text, fromEncoding="utf-8")
            # texts = response.xpath('//text()[not(ancestor::pre)]').extract()
            # for text in texts:
            #     text = self.cleanText(text)
            #     if len(text) != 0 and not self.isLineMatchCode(text):
            #         yield {
            #             # "projectRoot": projectRoot,
            #             "l": page,
            #             "t": text
            #         }
            soup = BeautifulSoup(response.text, fromEncoding="utf-8")
            texts = soup.find('html').text.split('\n')

            for text in texts:
                text = self.cleanText(text)
                if len(text) != 0 and not self.isLineMatchCode(text):
                    yield {
                        # "projectRoot": projectRoot,
                        "l": page,
                        "t": text
                    }
