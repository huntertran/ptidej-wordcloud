import random
import jsonpickle

from PIL import Image

jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False, indent=4)

# node.image = {
#   url: /* mandatory image URL */,
#   clip: /* Ratio of image clipping disk compared to node size (def 1.0) - see example to how we adapt this to differenmt shapes */,
#   scale: /* Ratio of how to scale the image, compared to node size, default 1.0 */,
#   w: /* numeric width - important for correct scaling if w/h ratio is not 1.0 */,
#   h: /* numeric height - important for correct scaling if w/h ratio is not 1.0 */
# }

class node_image(object):
    def __init__(self, url, w, h):
        self.url = url
        self.w = w
        self.h = h

class node(object):
    def __init__(self, id, label, x, y, size, color):
        self.id = id
        self.label = label
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.image = None


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
        new_node = node(linked_keyword.Id,
                        linked_keyword.Description,
                        x,
                        y,
                        10,
                        '#ff0000')
        self.nodes.append(new_node)

    def add_project(self, project, linked_keyword):
        x = random.randint(0, 30)
        y = random.randint(0, 30)

        new_node = node(project.Project,
                        project.Project,
                        x,
                        y,
                        5,
                        '#000000')

        image_path = './docs/images/shapes/' + project.Project + '.png'
        img = Image.open(image_path)
        w,h = img.size
        
        new_node.image = node_image(
            image_path,
            w,
            h
        )

        self.nodes.append(new_node)

        for relationship in project.relationships:
            new_edge = edge('e_' + project.Project + '_' + relationship,
                            relationship,
                            project.Project,
                            str(linked_keyword.Id),
                            2,
                            '#ff0000')
            self.edges.append(new_edge)

    def add_projects(self, linked_keyword):
        for project in linked_keyword.projects:
            res = any(node.id == project.Project for node in self.nodes)
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
            # for target in linked_keywords:
            #     if target.Id is not linked_keyword.Id:
            new_edge = edge('transparent_' + str(linked_keyword.Id),
                            '',
                            'trans',
                            str(linked_keyword.Id),
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
    with open('./docs/graph.json', 'w', encoding='utf8') as dataFile:
        dataFile.write(jsonpickle.encode(data, unpicklable=False))


def start_convert():
    linked_keywords = load_linked_result()

    graph = data()
    graph.parsed_result(linked_keywords)

    save_graph(graph)
