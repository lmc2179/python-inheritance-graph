import functools
import networkx
import inspect
import matplotlib.pyplot as plt
from collections import deque

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
    networkx.draw(inheritance_graph, layout, node_color='w', linewidths=0.0)
    networkx.draw_networkx_labels(inheritance_graph,pos=layout)
    plt.show()

def layout_factory(G):
    sorted_nodes = networkx.topological_sort(G)
    root = sorted_nodes[-1] # Assumes one connected component
    depth = 5
    return get_tree_layout(root, depth, G)

def _divide_line(l,r,n):
    if n < 0:
        return [] # This is a bit of a hack
    delta = (1.0*r-l)/(n+1)
    return [l + delta*i for i in range(0,n+2)]

def get_tree_layout(root, depth, G):
    delta = 1.0/(depth+1)
    node_groups = deque([[root]])
    group_bounds = deque([(0,1)])
    layout = {}
    y = 1.0
    while node_groups:
        for group, bound in zip(node_groups, group_bounds):
            x_layouts = _get_node_layouts(group, bound)
            for x,n in zip(x_layouts, group):
                layout[n] = (x, y*delta)
            child_groups = [G.predecessors(n) for n in group]
            child_bound_partitions = _divide_line(bound[0], bound[1], len(child_groups)-1)
            child_bounds = [(l,r) for l,r in zip(child_bound_partitions[:-1], child_bound_partitions[1:])]
            node_groups = deque(child_groups)
            group_bounds = deque(child_bounds)
        y -= 1
    return layout

def _get_node_layouts(group, bound):
    x_layout = _divide_line(bound[0], bound[1], len(group))
    return x_layout[1:-1]