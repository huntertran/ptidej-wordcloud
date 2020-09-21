# model for linked keyword json object

class LinkKeyword(object):
    def __init__(self, Id=None, Description=None, Keys=None):
        self.Id = Id
        self.Description = Description
        self.Keys = Keys
        # self.projects = []

    def decode_LinkKeyword(dict):
        return LinkKeyword(dict['id'], dict['description'], dict['keys'])

    # def addProject(self, project_name):
    #     self.projects.append(project_name)
