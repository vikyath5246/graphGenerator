import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel, LlavaForConditionalGeneration

model_name = "qizekun/ShapeLLM_7B_gapartnet_v1.0"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    use_fast=False,
    trust_remote_code=True
)

# Load model (uses GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Loading model...")
model = LlavaForConditionalGeneration.from_pretrained(model_name, trust_remote_code=True).to("cuda" if torch.cuda.is_available() else "cpu")

def initial_graph_shapellm(pcds):

    # Preparing the prompt
    system_part = (
        "You are an artificial intelligence assistant that is an expert in "
        "analyzing scenes for robotics based on data and your intelligence. "
        "You should stick to the output format without adding any assumptions or explanations."
    )
    
    user_part = (
        "I'll provide you a set of objects identified by ID. "
        "I want you to generate a scene graph with the objects as nodes and their relationships as edges. "
        "The dictionary has the format: {<obj_id>: <object_class>, [x_coord, y_coord, z_coord], pointcloud}"
        "Use this data to determine the most appropriate spatial relationships between objects. "
        "Some possible relationships are: in, out, on, up, down, under, beneath, below, above, over, around, "
        "between, beside, left, right, behind, ahead, front, back, top, bottom, across, by, near, close to, "
        "next to, with, against, beyond, far, among, middle, center, north, south, east, west, opposite, diagonal, "
        "inside, outside, touch, contains, holds, upside down, upright, right side up, turn, flip, rotate. "
        "Output the relationships strictly in the format: 'ObjectA, ObjectB, relationship'. "
        "Prepend 'EDGES:' before the lines of relationships. Provide no other text or assumptions. "
        "Here are the objects and point clouds:\n"
        f"data: {str(pcds)}\n"
    )
    
    # Combine into a single text prompt
    prompt = f"System: {system_part}\nUser: {user_part}\n"

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generate output
    output_ids = model.generate(
        **inputs, 
        max_new_tokens=256,
        temperature=0.7,
        do_sample=True
    )

    # Decode and print the output
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print(output_text)
    return output_text

