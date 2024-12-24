import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, class_name, id, **attributes):
        self.class_name = class_name
        self.id = id  # Unique identifier for the node
        self.attributes = attributes  # Dictionary of additional attributes

    def identifier(self):
        return f"{self.class_name}_{str(self.id)[:5]}"

    def __repr__(self):
        return f"Node({self.class_name}, {self.id}, {self.attributes})"
    
class Edge:
    def __init__(self, source, target, **attributes):
        self.source = source  # Source node identifier
        self.target = target  # Target node identifier
        self.attributes = attributes  # Dictionary of additional attributes

    def __repr__(self):
        return f"Edge({self.source} -> {self.target}, {self.attributes})"

def graphCreation(objects):
    G = nx.Graph()
    nodes = []
    edges = []
    for idx, object in enumerate(objects):

        node = Node(class_name=object['class_name'], id=object['id'])
        nodes.append(node)
        G.add_node(node.identifier(), **node.attributes)
        #G.add_node(str(object['class_name']) + "_"+ str(object['id'])[:5])
        if idx != 0:
            #G.add_edge(idx-1,idx)
            edge = Edge(source=nodes[idx - 1].identifier(), target=node.identifier())
            edges.append(edge)
            G.add_edge(edge.source, edge.target, **edge.attributes)

    plt.figure(figsize=(8, 6))  # Set the figure size
    pos = nx.spring_layout(G)  # Use spring layout for positioning the nodes
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=100, font_size=16, font_color="black", font_weight="bold", edge_color="gray")
    plt.title("Graph Visualization", fontsize=20)
    plt.show()