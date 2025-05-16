# graphGenerator

## What does graph generator do?

It create a scene graph from the result of concept graph, where nodes contain `class_name`, `id`, `center` and edges are relationships between these nodes.

* It takes in the result file from the concept graph
* It parses the result using the same object models from the concept graphs present in `/utils/conceptGraph`

In this code we have three ways to generate relationships (all the code resides in `/utils`):

- Through Perplexity API
- Through local LLMs (Mistral, Llama3)
- Through Heuristics

> **Note**: ShapeLLM doesn't work for our use‑case, as it has awareness of the object but not the scene. Usage of shapeLLM can be found on [this link](https://huggingface.co/qizekun/ShapeLLM_7B_gapartnet_v1.0)

### Relationship building workflow

1. First find all the objects present in the scene which are most relevant to our robotic tasks.  
2. Build relationships between these objects using the above methods.  
3. Create a graph using the NetworkX library.  
4. Visualise the generated graph.

## How to run the application

Firstly install all the required libraries. (Note: didn't have the time to create a requirement.txt file, so install dependencies one by one.)

```bash
python3 graphGenerator.py --result_path "<RESULT_PATH_FROM_CONCEPT_GRAPHS>"
```

Example:

```bash
python3 graphGenerator.py --result_path ./pcd_r_mapping_stride10.pkl.gz
```

### View in 3D (optional)

```bash
python3 mesh.py --result_path "<RESULT_PATH>"
```

Example:

```bash
python3 mesh.py --result_path ./pcd_r_mapping_stride10.pkl.gz
```

Sample result files can be found here: [Link](https://drive.google.com/drive/folders/1pPe23aHm4aEgwe-HOQJHRvp-Z8Olq5ia?usp=sharing)

## Future steps

* Current LLMs do not have very good spatial awareness, but they can identify objects relevant to robotic tasks.
* We can combine LLMs and heuristics, where an LLM selects the most relevant objects and our heuristics build relationships between those objects.
* While updating the relationships, we can optionally call the LLM for refinement.
* Include a .gitIgnore file
