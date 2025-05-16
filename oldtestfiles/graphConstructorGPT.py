import argparse
import networkx as nx
import matplotlib.pyplot as plt
import open3d as o3d

# Utility Functions
def parse_line(line):
    """ Parse the line to extract node data like node_id, clip_embedding, and reference frame """
    # Assuming the result file line format is something like: node_id, clip_embedding, reference_frame
    parts = line.strip().split(',')
    node_id = int(parts[0])
    clip_embedding = parts[1]  # Replace this with appropriate parsing logic
    reference_frame = parts[2]  # Replace this with appropriate parsing logic
    return node_id, clip_embedding, reference_frame

def extract_edge_info(line):
    """ Extract edge information from a line """
    # Assuming the edge format is: edge,source,target
    parts = line.strip().split(',')
    source = int(parts[1])
    target = int(parts[2])
    return source, target

def read_result_file(file_path):
    graph = nx.Graph()
    
    # Read and parse file to create graph
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('node'):
                node_id, clip_embedding, reference_frame = parse_line(line)
                graph.add_node(node_id, clip_embeddings=clip_embedding, base_object_reference_frame=reference_frame)
            elif line.startswith('edge'):
                source, target = extract_edge_info(line)
                graph.add_edge(source, target)
    
    return graph

def read_ply(ply_file_path):
    point_cloud = o3d.io.read_point_cloud(ply_file_path)
    return point_cloud

def read_rgbd(rgbd_file_path):
    # Implement RGBD file reading logic
    return None

# Visualizer Class
class Visualizer:
    def __init__(self, graph, point_cloud):
        self.graph = graph
        self.point_cloud = point_cloud

    def display(self):
        """ Display the graph and point cloud side by side """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Graph visualization on ax1
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, ax=ax1, with_labels=True, node_color='lightblue', edge_color='gray')

        # Point cloud visualization on ax2
        if self.point_cloud:
            vis = o3d.visualization.Visualizer()
            vis.create_window()
            vis.add_geometry(self.point_cloud)
            vis.run()
            vis.destroy_window()

        plt.show()

# Main Program
def main():
    parser = argparse.ArgumentParser(description='Graph SLAM Visualizer')
    parser.add_argument('--result_file', type=str, help='Path to the result file')
    parser.add_argument('--ply_file', type=str, help='Path to the point cloud (.ply) file')
    parser.add_argument('--rgbd_file', type=str, help='Path to the RGB+Depth image file')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode without visualization')

    args = parser.parse_args()

    # Read and build graph from file
    graph = nx.Graph()
    point_cloud = None
    
    if args.result_file:
        graph = read_result_file(args.result_file)
    elif args.ply_file:
        point_cloud = read_ply(args.ply_file)
    elif args.rgbd_file:
        rgbd_data = read_rgbd(args.rgbd_file)

    if args.headless:
        # Headless mode, print graph details
        print("Graph nodes:", graph.nodes(data=True))
        print("Graph edges:", graph.edges(data=True))
    else:
        # Initialize the visualizer for UI
        visualizer = Visualizer(graph, point_cloud)
        visualizer.display()

if __name__ == '__main__':
    main()
