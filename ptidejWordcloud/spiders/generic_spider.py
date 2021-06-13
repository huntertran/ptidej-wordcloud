import scrapy
import re
from bs4 import BeautifulSoup

from helpers.ProjectHelper import ProjectHelper


class GenericSpider(scrapy.Spider):
    name = "generic"

    def start_requests(self):
        site_url = getattr(self, 'site_url', None)
        existing_project_name = getattr(self, 'project_name', None)
        crawl_depth_level = int(getattr(self, 'crawl_depth_level', 0))

        request = scrapy.Request(site_url, callback=self.parse_root_url)
        request.cb_kwargs['root'] = self.extract_base_url(site_url)
        request.cb_kwargs['project_root'] = self.extract_project_root(site_url)
        request.cb_kwargs['level'] = crawl_depth_level
        request.cb_kwargs['current_level'] = 0
        request.cb_kwargs['project_name'] = ProjectHelper.get_project_name(site_url, existing_project_name)

        yield request

    def extract_base_url(self, url):
        fragments = url.split('/')
        return fragments[0] + "//" + fragments[2]

    def extract_project_root(self, url):
        fragments = url.split('/')
        root = fragments[0] + "//" + fragments[2]

        if len(fragments) == 3:
            return root
        else:
            return root + '/' + fragments[3]

    def parse_root_url(self, response, root, project_root, level, current_level, project_name):

        urls = []

        if hasattr(response, 'selector'):
            urls = response.selector.xpath("//a/@href").getall()

        for url in urls:
            if url.startswith('#') == False:
                url_to_scrap = self.build_url(root, url)
                # if root in urlToScrap:
                # if root in urlToScrap and project_name in urlToScrap.lower():
                if project_name in url_to_scrap.lower():

                    if type(current_level) is tuple:
                        current_level = current_level[0]

                    request = self.build_request(
                        root,
                        project_root,
                        url_to_scrap,
                        level,
                        current_level,
                        project_name)

                    yield request

        for item in self.parseUrl(response, project_root):
            yield item

    def build_request(self, root, project_root, url, level, current_level, project_name):
        if level == current_level:
            request = scrapy.Request(url, callback=self.parseUrl)
            request.cb_kwargs['project_root'] = project_root
        else:
            request = scrapy.Request(url, callback=self.parse_root_url)
            request.cb_kwargs['root'] = root
            request.cb_kwargs['project_root'] = project_root
            request.cb_kwargs['level'] = level
            request.cb_kwargs['current_level'] = current_level + 1,
            request.cb_kwargs['project_name'] = project_name
        return request

    def build_url(self, root, url):
        if url.startswith('http'):
            return url
        else:
            return root + url

    def clean_text(self, text):
        # remove all trailing whitespaces
        text = text.strip()
        # remove all redundant spaces
        text = re.sub(r'\s+', ' ', text)
        # remove newline chars
        text = text.strip('\r').strip('\n')

        return text

    def is_line_match_code(self, line):
        match_code = re.search(r'\S+\s?\{(.+)\}', line)
        if match_code:
            return True
        else:
            return False

    def parseUrl(self, response, project_root):
        page = response.url
        if 'text' in response.headers['Content-Type'].decode('utf-8'):
            soup = BeautifulSoup(response.text, fromEncoding="utf-8")

            html = soup.find('html')

            if not hasattr(html, 'text'):
                return

            texts = soup.find('html').text.split('\n')

            for text in texts:
                text = self.clean_text(text)
                if len(text) != 0 and not self.is_line_match_code(text):
                    yield {
                        "l": page,
                        "t": text
                    }
