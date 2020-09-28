# model for linked keyword json object

import json
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
        self.projects.append(link_project)


class LinkProject(object):
    def __init__(self, Project=None, Sentences=None):
        self.Project = Project
        self.Sentences = Sentences

    def decode_LinkProject(dict):
        return LinkProject(dict['project'], dict['sentences'])

    def add_sentence(self, sentence):
        if self.Sentences is None:
            self.Sentences = []
        self.Sentences.append(sentence)


class LinkKeywordEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
