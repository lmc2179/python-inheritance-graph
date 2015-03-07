import unittest
from python_inheritance_graph import InheritanceGraphMaker

class ModuleReadTest(unittest.TestCase):
    def test_module_read(self):
        import test_module
        inheritance_graph_maker = InheritanceGraphMaker()
        inheritance_graph_maker.add_module(test_module)
        inheritance_graph = inheritance_graph_maker.build_graph()
        print(inheritance_graph.node)
        print(inheritance_graph.edge)

if __name__ == '__main__':
    unittest.main()