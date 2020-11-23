# model for linked keyword json object

import numpy
from json import JSONEncoder

class LinkKeyword(object):
    def __init__(self, Id=None, Description=None, Keys=None):
        self.Id = Id
        self.Description = Description
        self.Keys = Keys
        self.projects = []

    def decode_LinkKeyword(dict):
        return LinkKeyword(dict['id'], dict['description'], dict['keys'])

    def add_link_project(self, link_project):

        for project in self.projects:
            if project.Project == link_project.Project:
                project.Sentences = project.Sentences + link_project.Sentences
                project.Sentences = numpy.unique(project.Sentences).tolist()
                return

        self.projects.append(link_project)


class LinkProject(object):
    def __init__(self, Project=None):
        self.Project = Project
        self.Sentences = []
        self.relationships = []

    def add_sentence(self, sentence):
        for sen in self.Sentences:
            if sen == sentence:
                return
        self.Sentences.append(sentence)
    
    def add_relationships(self, relationships):
        self.relationships = relationships


class LinkKeywordEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__