import openai
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from utils.openAI import initial_graph_relations, relations_update

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

    dic = {}

    for idx, obj in enumerate(objects):
        center_coordinates = obj['bbox'].center.tolist() if 'bbox' in obj else [0, 0, 0]
        node = Node(class_name=obj['class_name'], id=obj['id'], center=center_coordinates)
        nodes.append(node)
        G.add_node(node.identifier(), **node.attributes)

        dic[f"{obj['class_name']}_{str(obj['id'])[:5]}"] = [obj['class_name'], obj['bbox'].center.tolist() if 'bbox' in obj else [0, 0, 0]]

    relationships = initial_graph_relations(dic)

    for relationship in relationships:
        source_id, target_id, relation = relationship
        if source_id in G and target_id in G:
            G.add_edge(source_id, target_id, relationship=relation)
    #print(dic)
    return G

def process_action(G, action):
    # List to store edge details
    edge_details = []
    # List to store node details
    node_details = []

    # Extract edges with their relationship attributes
    for source, target, attributes in G.edges(data=True):
        relationship = attributes.get("relationship", None)
        edge_details.append([source, target, relationship])
    
    # Extract nodes with their attributes
    for node, attributes in G.nodes(data=True):
        node_class = attributes.get("class_name", None)
        node_id = attributes.get("id", None)
        coordinates = attributes.get("center", None)
        node_details.append([node_id, node_class, coordinates])
    
    new_relations = relations_update(node_details, edge_details, action)
    #print(new_relations)

    visualizeUpdatedGraph(G, new_relations)

    for change in new_relations:
        source_id, target_id, relationship, flag = change
        if source_id in G and target_id in G:
                # Check if the edge already exists
                if G.has_edge(source_id, target_id):
                    # Remove the old edge with its existing relationship
                    old_relationship = G[source_id][target_id].get('relationship')
                    if old_relationship:
                        G[source_id][target_id].pop('relationship')
                # Add the new edge with the new relationship
                G.add_edge(source_id, target_id, relationship=relationship)
        elif flag == 'remove':
            if G.has_edge(source_id, target_id):
                G.remove_edge(source_id, target_id)

    return G
    
def visualizeUpdatedGraph(G, edges):
    # Extract node positions from the 'center' attribute
    pos = {node: data['center'] for node, data in G.nodes(data=True)}

    # Prepare 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot nodes
    for node, (x, y, z) in pos.items():
        ax.scatter(x, y, z, s=100, label=node)  # Scatter plot for nodes

    # Plot edges
    for edge in edges:
        source = edge[0] 
        target = edge[1]
        source_pos = pos[source]
        target_pos = pos[target]
        edge_color = 'green'
        if edge[3] == 'remove':
            edge_color = 'red'
        ax.plot(
            [source_pos[0], target_pos[0]],
            [source_pos[1], target_pos[1]],
            [source_pos[2], target_pos[2]],
            color=edge_color,
            alpha=0.6,
        )

        # Annotate edges with relationships
        relationship = edge[2]
        mid_point = [
            (source_pos[0] + target_pos[0]) / 2,
            (source_pos[1] + target_pos[1]) / 2,
            (source_pos[2] + target_pos[2]) / 2,
        ]
        ax.text(
            mid_point[0], mid_point[1], mid_point[2],
            relationship,
            color='blue',
            fontsize=8,
        )

    for node, coord in pos.items():
        ax.scatter(coord[0], coord[1], coord[2], label=node, s=50)

    # Set plot labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Show plot
    #plt.legend()
    plt.title("3D Graph Visualization with afftected Relationships")
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()


def visualizeGraph(G):
    # Extract node positions from the 'center' attribute
    pos = {node: data['center'] for node, data in G.nodes(data=True)}

    # Prepare 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot nodes
    for node, (x, y, z) in pos.items():
        ax.scatter(x, y, z, s=100, label=node)  # Scatter plot for nodes

    # Plot edges
    for edge in G.edges():
        source, target = edge
        source_pos = pos[source]
        target_pos = pos[target]
        ax.plot(
            [source_pos[0], target_pos[0]],
            [source_pos[1], target_pos[1]],
            [source_pos[2], target_pos[2]],
            color='black',
            alpha=0.6,
        )

        # Annotate edges with relationships
        relationship = G.edges[source, target].get('relationship', 'undefined')
        mid_point = [
            (source_pos[0] + target_pos[0]) / 2,
            (source_pos[1] + target_pos[1]) / 2,
            (source_pos[2] + target_pos[2]) / 2,
        ]
        ax.text(
            mid_point[0], mid_point[1], mid_point[2],
            relationship,
            color='red',
            fontsize=8,
        )

    for node, coord in pos.items():
        ax.scatter(coord[0], coord[1], coord[2], label=node, s=50)

    # Set plot labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Show plot
    #plt.legend()
    plt.title("3D Graph Visualization with Relationships")
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()

def visualizeGraphOld(G):
    """Visualize the graph with relationships."""
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=100, 
            font_size=16, font_color="black", font_weight="bold", edge_color="gray")
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.title("Graph Visualization", fontsize=20)
    plt.show()
