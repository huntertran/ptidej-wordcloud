# model for linked keyword json object

import numpy
from json import JSONEncoder

class LinkKeyword(object):
    def __init__(self, id=None, description=None, keys=None):
        self.id = id
        self.description = description
        self.keys = keys
        self.projects = []

    @staticmethod
    def decode_object(dict):
        return LinkKeyword(dict['id'], dict['description'], dict['keys'])

    def add_link_project(self, link_project):

        for project in self.projects:
            if project.project == link_project.project:
                project.sentences = project.sentences + link_project.sentences
                project.sentences = numpy.unique(project.sentences).tolist()
                return

        self.projects.append(link_project)


class LinkProject(object):
    def __init__(self, project=None):
        self.project = project
        self.sentences = []
        self.relationships = []

    def add_sentence(self, sentence):
        for sen in self.sentences:
            if sen == sentence:
                return
        self.sentences.append(sentence)
    
    def add_relationships(self, relationships):
        self.relationships = relationships


class LinkKeywordEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__