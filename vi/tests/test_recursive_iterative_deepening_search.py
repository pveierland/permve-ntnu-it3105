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

#class TestRecursiveDepthLimitedSearch(unittest.TestCase):
#    def test_wtf(self):
#        x = vi.tree_node(42)
#        self.assertTrue(True)
#
#if __name__ == '__main__':
#    unittest.main()
