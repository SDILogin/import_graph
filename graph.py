class Node:
    def __init__(self, value):
        self.value = value
        self.out_edges = []

    def __eq__(self, node):
        if isinstance(node, Node):
            return node.value == self.value
        else:
            return self.value == node

    def add_out_edge_from_list(self, list_to):
        for to in list_to:
            self.add_out_edge(to)

    def add_out_edge(self, to):
        self.out_edges.add(to)

    def __str__(self):
        return str(self.value)

class Graph:
    def __init__(self, d_graph):
        self.nodes = []
        self.edges = []
        self.init_from_dict(d_graph)

    def init_from_dict(self, d):
        #import pdb
        #pdb.set_trace()
        for key in d:
            T = [x for x in self.nodes if x == key]
            if len(T) > 0:
                # used
                _from = T[0]
            else:
                # not used    
                _from = Node(key)
                self.nodes.append(_from)

            list_of_to_values = d[key]
            for _to_value in list_of_to_values:
                try:
                    _to = self.nodes[self.nodes.index(_to_value)]
                except ValueError:
                    _to = Node(_to_value)
                    self.nodes.append(_to)

                self.edges.append((_from, _to))


if __name__ == '__main__':
    G = Graph({1: [2,3,4], 2:[3,4], 3:[1,4]})
    print('nodes: ', *G.nodes)
    print('edges: ', [str(x[0])+'->'+str(x[1]) for x in G.edges])