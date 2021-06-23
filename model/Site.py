from collections import defaultdict


class Site(object):
    def __init__(self, is_crawled=None, crawl_depth_level=None, is_wordcloud_generated=None, site_url=None, project_name=None):
        self.is_crawled = is_crawled
        self.crawl_depth_level = crawl_depth_level
        self.is_wordcloud_generated = is_wordcloud_generated
        self.site_url = site_url
        self.project_name = project_name

    @staticmethod
    def decode_object(dict):
        if 'ProjectName' in dict:
            return Site(dict['IsCrawled'], dict['CrawlDepthLevel'], dict['IsWordcloudGenerated'], dict['SiteUrl'], dict['ProjectName'])
        else:
            return Site(dict['IsCrawled'], dict['CrawlDepthLevel'], dict['IsWordcloudGenerated'], dict['SiteUrl'])

    @staticmethod
    def encode_object(object):
        return {
            'IsCrawled': object.is_crawled,
            'CrawlDepthLevel': object.crawl_depth_level,
            'IsWordcloudGenerated': object.is_wordcloud_generated,
            'SiteUrl': object.site_url,
            'ProjectName': object.project_name
        }


class StemmedWord(object):
    def __init__(self, text=None, un_stemmed_word=None):
        self.un_stemmed = defaultdict(int)
        self.text = text
        self._count = 0
        self.add_un_stemmed(un_stemmed_word)

    def count(self):
        if self._count == 0:
            for un_stemmed in self.un_stemmed:
                self._count += self.un_stemmed[un_stemmed]

        return self._count

    def get_most_common_un_stemmed(self):
        return max(self.un_stemmed)

    def add_un_stemmed(self, un_stemmed):
        lower_un_stemmed = un_stemmed.lower()
        if not lower_un_stemmed in self.un_stemmed:
            self.un_stemmed[lower_un_stemmed] = 1
            # print("New unstemmed:" + unStemmed)
        else:
            self.un_stemmed[lower_un_stemmed] += 1
