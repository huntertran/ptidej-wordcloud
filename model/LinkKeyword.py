# model for linked keyword json object

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
    
    def encode_LinkProject(LinkProject_object):
        return {
            'project': LinkProject_object.Project,
            'sentences': LinkProject_object.Sentences
        }
    
    def decode_LinkProject(dict):
        return LinkProject(dict['project'], dict['sentences'])

    def add_sentence(sentence):
        self.Sentences.append(sentence)
