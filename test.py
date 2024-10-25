import networkx as nx
import matplotlib.pyplot as plt

# Define Node class with additional properties
class Node:
    def __init__(self, class_name, id, **attributes):
        self.class_name = class_name
        self.id = id  # Unique identifier for the node
        self.attributes = attributes  # Dictionary of additional attributes

    def identifier(self):
        return f"{self.class_name}_{str(self.id)[:5]}"

    def __repr__(self):
        return f"Node({self.class_name}, {self.id}, {self.attributes})"

# Define Edge class with additional properties
class Edge:
    def __init__(self, source, target, **attributes):
        self.source = source  # Source node identifier
        self.target = target  # Target node identifier
        self.attributes = attributes  # Dictionary of additional attributes

    def __repr__(self):
        return f"Edge({self.source} -> {self.target}, {self.attributes})"

# Graph creation function that uses Node and Edge classes
def graphCreation(objects):
    G = nx.Graph()
    
    # Create nodes and edges based on the objects
    nodes = []
    edges = []
    
    for idx, obj in enumerate(objects):
        # Create a new Node object
        node = Node(class_name=obj['class_name'], id=obj['id'])
        nodes.append(node)
        
        # Add node to the graph with its attributes
        G.add_node(node.identifier(), **node.attributes)
        
        # Connect nodes sequentially
        if idx != 0:
            # Create an edge from the previous node to the current node
            edge = Edge(source=nodes[idx - 1].identifier(), target=node.identifier())
            edges.append(edge)
            G.add_edge(edge.source, edge.target, **edge.attributes)

    # Draw the graph
    plt.figure(figsize=(8, 6))  # Set the figure size
    pos = nx.spring_layout(G)  # Use spring layout for positioning the nodes
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=100, font_size=16,
            font_color="black", font_weight="bold", edge_color="gray")
    plt.title("Graph Visualization", fontsize=20)
    plt.show()

# Example usage
objects = [
    {'class_name': 'Person', 'id': '123456'},
    {'class_name': 'Person', 'id': '234567'},
    {'class_name': 'Company', 'id': '345678'},
    {'class_name': 'Location', 'id': '456789'}
]

graphCreation(objects)
