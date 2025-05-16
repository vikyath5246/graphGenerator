"""
local_scene_graph.py
--------------------
$ pip install torch --index-url https://download.pytorch.org/whl/cu121
$ pip install transformers accelerate bitsandbytes optimum flash-attn
$ python local_scene_graph.py
"""
import torch, gc, json
from pathlib import Path
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
    Conversation,
)

# --------------------------------------------------------------------- #
# 1.  Pick one of your local checkpoints
# --------------------------------------------------------------------- #
MODEL_HUB_IDS = {
    "mistral":  "mistralai/Mistral-7B-Instruct-v0.3",
    "llama3":   "meta-llama/Meta-Llama-3-8B-Instruct",
    "phi3":     "microsoft/Phi-3-medium-4k-instruct",      # 14 B
    "qwen2":    "Qwen/Qwen2-VL-7B",                        # text‑only here
}
MODEL_CHOICE = "mistral"                                   # <<< change here

# --------------------------------------------------------------------- #
# 2.  One‑time model load (reuse the `generator` everywhere)
# --------------------------------------------------------------------- #
tokenizer = AutoTokenizer.from_pretrained(MODEL_HUB_IDS[MODEL_CHOICE])
model = AutoModelForCausalLM.from_pretrained(
    MODEL_HUB_IDS[MODEL_CHOICE],
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_4bit=True,
    attn_implementation="flash_attention_2",
)
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    # truncate when we hit “EDGES:” + newline twice
    eos_token_id=tokenizer.eos_token_id,
)

# --------------------------------------------------------------------- #
# 3.  A tiny helper that speaks “chat” for any model
# --------------------------------------------------------------------- #
def chat_completion(messages, max_new_tokens=256, temperature=0.2):
    """
    Very small wrapper around `pipeline` that converts
    ➜ list[{"role": ..., "content": ...}]  into one prompt string
    and decodes the answer.
    """
    sys_msg = next((m for m in messages if m["role"] == "system"), None)
    user_msgs = [m["content"] for m in messages if m["role"] == "user"]

    # Basic prompt template that works well for most instruct models
    prompt = ""
    if sys_msg:
        prompt += f"<|system|>\n{sys_msg['content']}\n<|end|>\n"
    for m in user_msgs:
        prompt += f"<|user|>\n{m}\n<|end|>\n"
    prompt += "<|assistant|>\n"

    out = generator(
        prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )[0]["generated_text"]

    # Keep only the assistant part
    return out.split("<|assistant|>")[-1].strip()

# --------------------------------------------------------------------- #
# 4.  Your two functions, unchanged in spirit, now fully local
# --------------------------------------------------------------------- #
def initial_graph_relations(node_data: dict):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial‑intelligence assistant that is an expert in "
                "analyzing scenes for robotics. Stick to the output format without "
                "adding any assumptions or explanations."
            ),
        },
        {
            "role": "user",
            "content": (
                "I'll give you a list of objects and their coordinates in a scene. "
                "Generate a scene graph with each object as a node and edges as "
                "relationships. Use only the most appropriate relationships.\n"
                "Input format: {id: [class, [x, y, z]]}\n"
                "Output format: ObjectA, ObjectB, relationship\n"
                "Return the list prefixed by 'EDGES:' and nothing else.\n"
                f"Possible relationships: In, out, on, up, down, under, above, over, "
                "around, between, beside, left, right, behind, front, back, by, near, "
                "next to, with, against, beyond, among, inside, outside, touch, contains, "
                "holds, upside down, upright, rotate.\n"
                f"data = {json.dumps(node_data)}"
            ),
        },
    ]

    raw = chat_completion(messages)
    # Parse
    lines = raw.split("EDGES:")[-1].strip().split("\n")
    edges = [line.lstrip("- ").split(",") for line in lines if line]
    edges = [[s.strip() for s in triple] for triple in edges]
    return edges


def relations_update(nodes, edges, action):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial‑intelligence assistant that is an expert in "
                "analyzing scenes for robotics. Stick to the output format without "
                "adding any assumptions or explanations."
            ),
        },
        {
            "role": "user",
            "content": (
                "Given an action, a list of nodes, and current edges, output the "
                "updated edges affected by the action.\n"
                "Node format: [id, class, [x, y, z]]\n"
                "Edge format: [source, target, relation]\n"
                "Action: plain text\n"
                "Return rows as 'source, target, relation, flag' where flag is ADD/REMOVE, "
                "prefixed by 'EDGES:' and nothing else.\n"
                "Possible relationships: In, out, on, up, down, under, above, over, "
                "around, between, beside, left, right, behind, front, back, by, near, "
                "next to, with, against, beyond, among, inside, outside, touch, contains, "
                "holds, upside down, upright, rotate.\n"
                f"nodes = {json.dumps(nodes)}\n"
                f"edges = {json.dumps(edges)}\n"
                f"action = \"{action}\""
            ),
        },
    ]

    raw = chat_completion(messages)
    # Parse
    lines = raw.split("EDGES:")[-1].strip().split("\n")
    upd = [line.lstrip("- ").split(",") for line in lines if line]
    upd = [[s.strip() for s in quad] for quad in upd]
    return upd

# --------------------------------------------------------------------- #
# 5.  Quick smoke‑test
# --------------------------------------------------------------------- #
if __name__ == "__main__":
    sample_nodes = {
        "1": ["cup",  [0.2, 0.1, 0.0]],
        "2": ["table",[0.0, 0.0, 0.0]],
        "3": ["plate",[0.1, 0.1, 0.01]],
    }
    print(">>> initial_graph_relations")
    print(initial_graph_relations(sample_nodes))

    print("\n>>> relations_update")
    node_list  = [["1","cup",[0.2,0.1,0.0]],["2","table",[0.0,0.0,0.0]]]
    edge_list  = [["cup","table","on"]]
    action_txt = "The robot lifts the cup off the table."
    print(relations_update(node_list, edge_list, action_txt))

    # Clean‑up VRAM if you run this repeatedly
    torch.cuda.empty_cache(); gc.collect()
