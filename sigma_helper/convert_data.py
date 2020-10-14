import random
import jsonpickle

jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)


class node(object):
    def __init__(self, id, label, x, y, size):
        self.id = id
        self.label = label
        self.x = x
        self.y = y
        self.size = size


class edge(object):
    def __init__(self, id, source, target):
        self.id = id
        self.source = source
        self.target = target


class data(object):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_key(self, linked_keyword):
        x = random.randint(0, 30)
        y = random.randint(0, 30)
        new_node = node(linked_keyword.Id,
                        linked_keyword.Description,
                        x,
                        y,
                        10)
        self.nodes.append(new_node)

    def add_project(self, project, linked_keyword):
        x = random.randint(0, 30)
        y = random.randint(0, 30)
        new_node = node(project.Project,
                        project.Project,
                        x,
                        y,
                        5)
        self.nodes.append(new_node)

        for relationship in project.relationships:
            new_edge = edge('e_' + project.Project + '_' + relationship,
                            project.Project,
                            linked_keyword.Id)
            self.edges.append(new_edge)

    def add_projects(self, linked_keyword):
        for project in linked_keyword.projects:
            res = any(node.id == project.Project for node in self.nodes)
            if not res:
                self.add_project(project, linked_keyword)

    def parsed_result(self, linked_keywords):
        for linked_keyword in linked_keywords:
            self.add_key(linked_keyword)
            self.add_projects(linked_keyword)


def load_linked_result():
    file_path = './data/linked.json'
    with open(file_path, 'r', encoding='utf8') as dataFile:
        return jsonpickle.decode(dataFile.read())


def save_graph(data):
    with open('./docs/graph.json', 'w', encoding='utf8') as dataFile:
        dataFile.write(jsonpickle.encode(data))


def start_convert():
    linked_keywords = load_linked_result()

    graph = data()
    graph.parsed_result(linked_keywords)

    save_graph(graph)
