import unittest
import python_inheritance_graph

class ModuleReadTest(unittest.TestCase):
    def test_module_read(self):
        import test_module
        inheritance_graph_maker = python_inheritance_graph.InheritanceGraphMaker()
        inheritance_graph_maker.add_module(test_module)
        inheritance_graph = inheritance_graph_maker.build_graph()
        print(inheritance_graph.node)

    def test_module_draw(self):
        import test_module
        inheritance_graph_maker = python_inheritance_graph.InheritanceGraphMaker()
        inheritance_graph_maker.add_module(test_module)
        inheritance_graph = inheritance_graph_maker.build_graph()
        python_inheritance_graph.draw(inheritance_graph)


if __name__ == '__main__':
    unittest.main()