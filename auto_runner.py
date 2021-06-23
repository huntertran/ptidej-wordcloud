import json
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from nlp.NlpProcessing import process
from model.Site import Site
from nlp.Linker import create_link
from nlp.SentenceAnalyzer import start_analyze
from sigma_helper.convert_data import start_convert


settings = get_project_settings()
configure_logging(settings=settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl(file_path):

    crawler = runner.spider_loader.list()[0]

    # file_path = './data/sitelist.json'

    with open(file_path, 'r') as dataFile:
        site_data_list = json.load(dataFile, object_hook=Site.decode_object)

    index = 0
    for site in site_data_list:

        # Crawling
        if not site.is_crawled:
            # TODO: edit here to stop re-scraping a site on different run
            site_data_list[index].is_crawled = True
            yield runner.crawl(crawler, site_url=site.site_url, project_name=site.project_name, crawl_depth_level=site.crawl_depth_level)
        index += 1

    with open(file_path, 'w') as dataFile:
        json.dump(site_data_list, dataFile, default=Site.encode_object, indent=4)

    if reactor.running:
        reactor.stop()
    else:
        yield runner.crawl(crawler, site_url="http://www.msftconnecttest.com/connecttest.txt", project_name="", crawl_depth_level=0)
        reactor.stop()


def nlp(file_path):
    # file_path = './data/sitelist.json'

    with open(file_path, 'r') as data_file:
        site_data_list = json.load(data_file, object_hook=Site.decode_object)

    index = 0
    for site in site_data_list:
        # NLP Processing
        if not site.is_wordcloud_generated:
            process(site.site_url, site.project_name)
            site_data_list[index].is_wordcloud_generated = True
        index += 1

    with open(file_path, 'w') as data_file:
        json.dump(site_data_list, data_file, default=Site.encode_object, indent=4)


crawl("./input/sitelist.json")
reactor.run()

nlp("./input/sitelist.json")
create_link("./input/sitelist.json", "./input/link_keyword.json")
start_analyze()
start_convert()