import os
import pickle
import gzip
import argparse

from utils.conceptGraph.slam_classes import MapObjectList
from utils.edgeUpdate import graphCreation, process_action, visualizeGraph

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result_path", type=str, default=None)
    return parser

def load_result(result_path):
    # check if theres a potential symlink for result_path and resolve it
    potential_path = os.path.realpath(result_path)
    if potential_path != result_path:
        print(f"Resolved symlink for result_path: {result_path} -> \n{potential_path}")
        result_path = potential_path
    with gzip.open(result_path, "rb") as f:
        results = pickle.load(f)

    if not isinstance(results, dict):
        raise ValueError("Results should be a dictionary! other types are not supported!")
    
    objects = MapObjectList()
    objects.load_serializable(results["objects"])
    objects_in_frame = MapObjectList()
    objects_in_frame.extend(obj for obj in objects if not obj['is_background'])

    G = graphCreation(objects_in_frame)
    visualizeGraph(G=G)

    while(True):
        action = input("Enter your action here: ")
        if action == 'q':
            break
        G = process_action(G, str(action))
    visualizeGraph(G=G)

def main(args):
    result_path = args.result_path
    
    assert not (result_path is None and rgb_pcd_path is None), \
        "Either result_path or rgb_pcd_path must be provided."
        
    load_result(result_path)
    
if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)

'''

python3 graphGenerator.py --result_path ./pcd_r_mapping_stride10.pkl.gz

'''
