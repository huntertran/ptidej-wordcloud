from collections import defaultdict


class Site(object):
    def __init__(self, IsCrawled=None, CrawlDepthLevel=None, IsWordcloudGenerated=None, SiteUrl=None):
        self.IsCrawled = IsCrawled
        self.CrawlDepthLevel = CrawlDepthLevel
        self.IsWordcloudGenerated = IsWordcloudGenerated
        self.SiteUrl = SiteUrl

    def decode_Site(dict):
        return Site(dict['IsCrawled'], dict['CrawlDepthLevel'], dict['IsWordcloudGenerated'], dict['SiteUrl'])

    def encode_Site(siteObject):
        return {
            'IsCrawled': siteObject.IsCrawled,
            'CrawlDepthLevel': siteObject.CrawlDepthLevel,
            'IsWordcloudGenerated': siteObject.IsWordcloudGenerated,
            'SiteUrl': siteObject.SiteUrl
        }


class StemmedWord(object):
    def __init__(self, Text=None, UnStemmedWord=None):
        self.UnStemmed = defaultdict(int)
        self.Text = Text
        self._count = 0
        self.addUnStemmed(UnStemmedWord)

    def count(self):
        if self._count == 0:
            for unStemmed in self.UnStemmed:
                self._count += self.UnStemmed[unStemmed]

        return self._count

    def getMostCommonUnStemmed(self):
        return max(self.UnStemmed)

    def addUnStemmed(self, unStemmed):
        lowerUnStemmed = unStemmed.lower()
        if not lowerUnStemmed in self.UnStemmed:
            self.UnStemmed[lowerUnStemmed] = 1
            # print("New unstemmed:" + unStemmed)
        else:
            self.UnStemmed[lowerUnStemmed] += 1
            # if self.UnStemmed[unStemmed] > 0:
            #     print("Unstemmed Counted:" + str(self.UnStemmed[unStemmed]) + "|" + unStemmed)
