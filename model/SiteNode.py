from dataclasses import dataclass

@dataclass
class SiteNode(object):
    index: int
    key: str

    def __init__(self, index=0, key=None):
        self.index = index
        self.key = key