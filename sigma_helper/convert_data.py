import random
import jsonpickle

from PIL import Image

jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False, indent=4)

class node_image(object):
    def __init__(self, url, w, h):
        self.url = url
        self.w = w
        self.h = h
        self.scale = 1

class node(object):
    def __init__(self, id, label, x, y, size, color):
        self.id = id
        self.label = label
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.image = None
        self.type = 'def'


class edge(object):
    def __init__(self, id, label, source, target, size, color):
        self.id = id
        self.label = label
        self.source = source
        self.target = target
        self.size = size
        self.type = 'curvedArrow'
        self.color = color


class data(object):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_key(self, linked_keyword):
        x = random.randint(0, 30)
        y = random.randint(0, 30)
        new_node = node(linked_keyword.id,
                        linked_keyword.description,
                        x,
                        y,
                        10,
                        '#0000ff')
        self.nodes.append(new_node)

    def add_project(self, project, linked_keyword):
        x = random.randint(0, 30)
        y = random.randint(0, 30)

        new_node = node(project.project,
                        project.project,
                        x,
                        y,
                        5,
                        '#000000')

        image_path = 'images/shapes/thumbnails/' + project.project + '.png'
        actual_image_path = './docs/' + image_path

        img = Image.open(actual_image_path)
        w,h = img.size
        
        new_node.image = node_image(
            image_path,
            w,
            h
        )

        new_node.type = 'image'

        self.nodes.append(new_node)

        for relationship in project.relationships:
            new_edge = edge('e_' + project.project + '_' + relationship,
                            relationship,
                            project.project,
                            str(linked_keyword.Id),
                            2,
                            '#0000ff')
            self.edges.append(new_edge)

    def add_projects(self, linked_keyword):
        for project in linked_keyword.projects:
            res = any(node.id == project.project for node in self.nodes)
            if not res:
                self.add_project(project, linked_keyword)

    def add_transparent_link_between_keys(self, linked_keywords):
        # transparent node
        transparent_node = node('trans',
                                '',
                                30,
                                30,
                                1,
                                '#00000000')

        self.nodes.append(transparent_node)

        for linked_keyword in linked_keywords:
            new_edge = edge('transparent_' + str(linked_keyword.id),
                            '',
                            'trans',
                            str(linked_keyword.id),
                            0.2,
                            '#00000000')
            self.edges.append(new_edge)

    def parsed_result(self, linked_keywords):
        for linked_keyword in linked_keywords:
            self.add_key(linked_keyword)
            self.add_projects(linked_keyword)
        self.add_transparent_link_between_keys(linked_keywords)


def load_linked_result():
    file_path = './data/linked.json'
    with open(file_path, 'r', encoding='utf8') as dataFile:
        return jsonpickle.decode(dataFile.read())


def save_graph(data):
    with open('./docs/data/graph.json', 'w', encoding='utf8') as dataFile:
        dataFile.write(jsonpickle.encode(data, unpicklable=False))


def start_convert():
    linked_keywords = load_linked_result()

    graph = data()
    graph.parsed_result(linked_keywords)

    save_graph(graph)
