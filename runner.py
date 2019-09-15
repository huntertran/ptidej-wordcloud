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
            'site_url=0,0,https://www.eclipse.org/paho/'
            # '-o',
            # 'out.json'
        ]
    )
except SystemExit:
    pass