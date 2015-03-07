import networkx
import inspect

class InheritanceGraphMaker(object):
    def __init__(self):
        self.class_list = []

    def build_graph(self):
        G = networkx.DiGraph()
        G.add_nodes_from(self.class_list)
        edges = [(cls, cls.__bases__) for cls in self.class_list]
        [G.add_edge(subclass, superclass) for subclass, superclass in edges]
        return G

    def add_module(self, module):
        classes = self._get_classes_from_module(module)
        [self.add_class(cls) for cls in classes]

    def _get_classes_from_module(self, module):
        return [obj for name, obj in inspect.getmembers(module) if inspect.isclass(obj)]

    def add_class(self, cls):
        self.class_list.append(cls)