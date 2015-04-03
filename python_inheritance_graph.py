import functools
import networkx
import inspect
import matplotlib.pyplot as plt

class InheritanceGraphMaker(object):
    def __init__(self):
        self.class_list = []

    def build_graph(self):
        G = networkx.DiGraph()
        G.add_nodes_from(self.class_list)
        edges = [(cls, base_class) for cls in self.class_list for base_class in cls.__bases__]
        [G.add_edge(subclass, superclass) for subclass, superclass in edges]
        return G

    def add_module(self, module):
        classes = self._get_classes_from_module(module)
        [self.add_class(cls) for cls in classes]

    def _get_classes_from_module(self, module):
        return [obj for name, obj in inspect.getmembers(module) if inspect.isclass(obj)]

    def add_class(self, cls):
        self.class_list.append(cls)

def draw(inheritance_graph):
    layout = layout_factory(inheritance_graph)
    networkx.draw(inheritance_graph, layout)
    networkx.draw_networkx_labels(inheritance_graph,pos=layout)
    plt.show()

def layout_factory(G):
    sorted_nodes = networkx.topological_sort(G)
    root = sorted_nodes[-1] # Assumes one connected component
    depth = 5
    return get_tree_layout(root, depth, G)

def _divide_line(l,r,n):
    delta = (1.0*r-l)/(n+1)
    return [l + delta*i for i in range(0,n+2)]

def get_tree_layout(root, depth, G):
    delta = 1.0/(depth+1)
    nodes = [[root]]
    bounds = [(0,1)]
    layout = {}
    y = 1.0
    while nodes and all([len(group) > 0 for group in nodes]):
        x_layouts = _get_node_layouts(nodes, bounds)
        for x,n in zip(x_layouts, reduce_list(nodes)):
            layout[n] = (x, y*delta)
        nodes, bounds = _get_next_level(reduce_list(nodes), G)
        y -= 1
    return layout

def _get_node_layouts(node_groups, group_bounds):
    x_groups = [_divide_line(b[0], b[1], len(g)) for g,b in zip(node_groups, group_bounds)]
    x_layout = reduce_no_duplicates(x_groups)
    return x_layout[1:-1]

def _get_next_level(nodes, G):
    next_level_groups = [G.predecessors(n) for n in nodes]
    #TODO: Group bounds should be within previous group bounds
    group_boundaries = _divide_line(0.0, 1.0, len(next_level_groups)-1)
    new_bounds = list(zip(group_boundaries[:-1], group_boundaries[1:]))
    return next_level_groups, new_bounds

def reduce_list(L):
    return functools.reduce(lambda l1,l2:l1+l2, L)

def reduce_no_duplicates(L):
    unique_reduced_L = []
    for element in reduce_list(L):
        if not unique_reduced_L or unique_reduced_L[-1] != element:
            unique_reduced_L.append(element)
    return unique_reduced_L

