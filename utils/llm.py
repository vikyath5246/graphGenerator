from openai import OpenAI
import json
import pickle
import ast


YOUR_API_KEY = "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"

def initial_graph_relations(node_data):

    messages = [
        {
            "role": "system",
            "content": (
                "You are an artifical intelligence assistant that is an expert in analyzing scenes for robotics based on data and your intelligence. You should stick to the output format without adding any assumptions or explanations"
            )
        },
        {
            "role": "user",
            "content": (
                "i'll give you a list of objects and their coordinates in a scene. I am looking to generate a scene graph with object as a node and edge as a relationship between the nodes. Give only the most appropriate relationships in the form of text using intelligence."
                "The format of the input is gonna be {\"id_of_object\": ['class_of_object', [x_coord, y_coord, z_coord], ....}"
                "output format should be Object_a, object_b, relationship"
                "Just give me the output in the form of ['Object_A, 'Object_B, relationship] without any other text or assumptions."
                "Some possible relationships are: In, out,  on, up, down, under, beneath, below, above,  over, around, between, beside, left, right, behind, ahead, front, back, top, bottom, across, by, near, close to, next to, with, against, beyond, near, far, among, middle, center, north, south, east, west, opposite, diagonal, here, there, anywhere,  inside, outside,  touch, contains, holds, upside down, upright, right side up, turn, flip, rotate."
                "Append EDGES: before the actual output. Don't forget to add edges."
                "data is: " + str(node_data)
            )
        }
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")
    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,
    )
    out = (response.choices[0].message.content)
    real_edges = out.split('EDGES:')[1].split('\n')
    ans = []
    for s in real_edges:
        tmp = []
        if s[0:2] == '- ':
            kek = s[2:].split(',')
            for i in kek:
                tmp.append(i.strip(' '))
            ans.append(tmp)
    return ans

def relations_update(nodes, edges, action):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artifical intelligence assistant that is an expert in analyzing scenes for robotics based on data and your intelligence. You should stick to the output format without adding any assumptions or explanations"
            )
        },
        {
            "role": "user",
            "content": (
                "I'll give you an action and list of objects and their coordinates in a scene and another list of list of edge relations containing source, traget, relation."
                "The format of the input for node is gonna be [\"id_of_object\", 'class_of_object', [x_coord, y_coord, z_coord]] and here is the data " + str(nodes) + 
                ",The format of the input for edge relations is gonna be [source, target, relation] and here is the data " + str(edges) + 
                ",The format of input for action is a text and here is the action " + str(action) +
                ". Based on the action figure out the most approriate nodes and update the relations that is add edges and remove edges between the nodes affected by the action."
                "output format should be source, target, relationship, flag. flag says if we are adding or removing the edge"
                "Just give me the output in the form of 'source, 'target, relationship, flag without any other text or assumptions."
                "Some possible relationships are: In, out,  on, up, down, under, beneath, below, above,  over, around, between, beside, left, right, behind, ahead, front, back, top, bottom, across, by, near, close to, next to, with, against, beyond, near, far, among, middle, center, north, south, east, west, opposite, diagonal, here, there, anywhere,  inside, outside,  touch, contains, holds, upside down, upright, right side up, turn, flip, rotate."
                "Append EDGES: before the actual output. Don't forget to add this."
            )
        }
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")
    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,
    )
    out = (response.choices[0].message.content)
    #print(out)
    # Split the text into lines and remove "EDGES:" and empty lines
    lines = out.strip().split("\n")[1:]

    # Process each line into a list of attributes
    new_edges = [line.strip().split(", ") for line in lines]
    return new_edges
    # new_edges = out.split('EDGES:')[1].split('\n')
    # ans = []
    # for s in new_edges:
    #     tmp = []
    #     if s[0:2] == '- ':
    #         kek = s[2:].split(',')
    #         for i in kek:
    #             tmp.append(i.strip(' '))
    #         ans.append(tmp)
    #     elif s[0:5]  != 'EDGES' :
    #         kek = s.split(',')
    #         for i in kek:
    #             tmp.append(i.strip(' '))
    #         ans.append(tmp)
    # return ans