import vi

def build_romania_graph():
    return vi.graph([
        [ 'Sibiu',          'Rimnicu Vilcea', 80 ],
        [ 'Sibiu',          'Fagaras',        99 ],
        [ 'Fagaras',        'Bucharest',     211 ],
        [ 'Rimnicu Vilcea', 'Pitesti',        97 ],
        [ 'Pitesti',        'Bucharest',     101 ]])

def test_wtf():
    graph = build_romania_graph()
    problem = vi.graph_search_problem(
        graph, graph.lookup('Sibiu'), graph.lookup('Bucharest'))
    print(graph)
    print(vi.breadth_first_search(problem))

#class TestRecursiveDepthLimitedSearch(unittest.TestCase):
#    def test_wtf(self):
#        x = vi.tree_node(42)
#        self.assertTrue(True)
#
#if __name__ == '__main__':
#    unittest.main()
