import networkx as nx
import matplotlib.pyplot as plt

# Function to construct a simple graph
def create_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 4), (3, 4), (4, 5)])
    return G

# Draw the graph
def visualise_graph(Graph):
    plt.figure(figsize=(8, 6))  # Set the figure size
    pos = nx.spring_layout(Graph)  # Use spring layout for positioning the nodes
    nx.draw(Graph, pos, with_labels=True, node_color="skyblue", node_size=1000, font_size=16, font_color="black", font_weight="bold", edge_color="gray")
    plt.title("Graph Visualization", fontsize=20)
    plt.show()

# Depth First Search using networkx
def dfs(graph, start):
    visited = set()
    result = []
    
    def dfs_recursive(node):
        if node not in visited:
            visited.add(node)
            result.append(node)
            for neighbor in graph.neighbors(node):
                dfs_recursive(neighbor)

    dfs_recursive(start)
    return result

# Breadth First Search using networkx
def bfs(graph, start):
    visited = set()
    queue = [start]
    result = []

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            result.append(node)
            queue.extend(set(graph.neighbors(node)) - visited)

    return result

# Find connected components in the graph
def connected_components(graph):
    return list(nx.connected_components(graph))

# Check if a graph has cycles
def is_cyclic(graph):
    try:
        cycle = nx.find_cycle(graph)
        return True, cycle
    except nx.exception.NetworkXNoCycle:
        return False, []

if __name__ == "__main__":
    G = create_graph()

    visualise_graph(Graph=G)

    print("Graph Nodes:", G.nodes())
    print("Graph Edges:", G.edges())

    # Perform DFS
    dfs_result = dfs(G, 0)
    print("DFS Traversal:", dfs_result)

    # Perform BFS
    bfs_result = bfs(G, 0)
    print("BFS Traversal:", bfs_result)

    # Find connected components
    components = connected_components(G)
    print("Connected Components:", components)

    # Check if the graph has cycles
    has_cycle, cycle = is_cyclic(G)
    print(f"Graph has a cycle: {has_cycle}")
    if has_cycle:
        print("Cycle found:", cycle)
