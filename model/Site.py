class Site(object):
    def __init__(self, IsCrawled=None, CrawlDepthLevel=None, IsWordcloudGenerated=None, SiteUrl=None):
        self.IsCrawled = IsCrawled
        self.CrawlDepthLevel = CrawlDepthLevel
        self.IsWordcloudGenerated = IsWordcloudGenerated
        self.SiteUrl = SiteUrl
    def decode_Site(dict):
        return Site(dict['IsCrawled'],dict['CrawlDepthLevel'],dict['IsWordcloudGenerated'],dict['SiteUrl'])
    # def encode_Site(siteObject):
    #     return (siteObject.IsCrawled, siteObject.CrawlDepthLevel, siteObject.IsWordcloudGenerated, siteObject.SiteUrl)