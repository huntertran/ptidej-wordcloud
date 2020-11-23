import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'generic',
            '-a'
            'site_url=https://www.eclipse.org/paho/',
            '-a'
            'crawlDepthLevel=0'
            # '-o',
            # 'out.json'
        ]
    )
except SystemExit:
    pass
