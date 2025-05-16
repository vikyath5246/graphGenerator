#!/usr/bin/env python3
"""
Scene‑Graph Heuristics — **Single‑Edge / `relationship` Attribute**
=================================================================
* Returns an **`nx.DiGraph`** (not MultiDiGraph) so `.edges[u,v]` works with
  exactly two indices — matching the caller’s expectation.
* Every edge carries a **single** attribute named **`relationship`** (not
  `relation`). If more than one heuristic fires for the same ordered pair we
  **keep the first hit**; feel free to change that policy.
* Nodes expose only `class_name`, `id`, and `center`.

```python
from heuristics import graph_relations
G = graph_relations(raw_objects)  # ready for visualizeGraph()
```
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

import numpy as np
import networkx as nx

# ────────────────────────────────────────────────── Constants ──┐
EPS_H       = 0.05          # 5 cm contact tolerance
K_NEAR      = 4.0           # near if < 4× longer edge
K_FAR_RATIO = 0.75          # far if > 75 % room diag
# ────────────────────────────────────────────────────────────────┘

# ───────────────────────────────────────── Box wrapper ─────────
@dataclass
class Box:
    class_name: str
    center: np.ndarray     # shape (3,)
    half_extent: np.ndarray  # shape (3,)

    @property
    def aabb(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.center - self.half_extent, self.center + self.half_extent

    @property
    def long_edge(self) -> float:
        return float(self.half_extent.max() * 2.0)

# ─────────────────────────────────────────── Metrics ───────────

def horiz_overlap(b1: Box, b2: Box, axis: int) -> float:
    min1, max1 = b1.aabb
    min2, max2 = b2.aabb
    inter = max(0.0, min(max1[axis], max2[axis]) - max(min1[axis], min2[axis]))
    span = max(max1[axis], max2[axis]) - min(min1[axis], min2[axis]) + 1e-6
    return inter / span


def vert_gap(top: Box, bottom: Box) -> float:
    return top.aabb[0][2] - bottom.aabb[1][2]


def center_delta(a: Box, b: Box) -> np.ndarray:
    return b.center - a.center


def euclid(a: Box, b: Box) -> float:
    return float(np.linalg.norm(center_delta(a, b)))

# ───────────────────────────── Relationship rules ─────────────

def relationships(a: Box, b: Box, room_diag: float) -> List[Tuple[str, str, str]]:
    """Return **directed** relations (u, v, rel)."""
    dx, dy, _ = center_delta(a, b)
    out: List[Tuple[str, str, str]] = []

    # contact
    if horiz_overlap(a, b, 0) > 0.3 and horiz_overlap(a, b, 1) > 0.3:
        if 0 <= vert_gap(b, a) <= EPS_H:
            out.append((a_key, b_key, "on"))
            out.append((b_key, a_key, "under"))
        elif 0 <= vert_gap(a, b) <= EPS_H:
            out.append((a_key, b_key, "under"))
            out.append((b_key, a_key, "on"))

    # vertical ordering
    if vert_gap(b, a) > a.half_extent[2] * 0.5:
        out.append((a_key, b_key, "above"))
        out.append((b_key, a_key, "below"))
    elif vert_gap(a, b) > b.half_extent[2] * 0.5:
        out.append((a_key, b_key, "below"))
        out.append((b_key, a_key, "above"))

    # lateral
    if abs(dx) > max(a.half_extent[0], b.half_extent[0]) * 0.5:
        if dx > 0:
            out.append((a_key, b_key, "right"))
            out.append((b_key, a_key, "left"))
        else:
            out.append((a_key, b_key, "left"))
            out.append((b_key, a_key, "right"))
    if abs(dy) > max(a.half_extent[1], b.half_extent[1]) * 0.5:
        if dy > 0:
            out.append((a_key, b_key, "behind"))
            out.append((b_key, a_key, "front"))
        else:
            out.append((a_key, b_key, "front"))
            out.append((b_key, a_key, "behind"))

    # distance
    d = euclid(a, b)
    if d < K_NEAR * min(a.long_edge, b.long_edge):
        out.append((a_key, b_key, "near"))
        out.append((b_key, a_key, "near"))
    elif d > K_FAR_RATIO * room_diag:
        out.append((a_key, b_key, "far"))
        out.append((b_key, a_key, "far"))

    # containment
    amin, amax = a.aabb
    bmin, bmax = b.aabb
    if np.all(bmin >= amin) and np.all(bmax <= amax):
        out.append((a_key, b_key, "contains"))
        out.append((b_key, a_key, "inside"))
    elif np.all(amin >= bmin) and np.all(amax <= bmax):
        out.append((a_key, b_key, "inside"))
        out.append((b_key, a_key, "contains"))

    return out

# ─────────────────────────── Input conversion helper ──────────

def _as_box(key: str, value: Any) -> Box:
    if isinstance(value, Box):
        return value

    if not (isinstance(value, (list, tuple)) and len(value) == 2):
        raise ValueError(f"Bad value for {key}: {value}")

    cls, geom = value

    if hasattr(geom, "center") and hasattr(geom, "extent"):
        center = np.asarray(geom.center, float)
        half_extent = np.asarray(geom.extent, float) / 2.0
        return Box(cls, center, half_extent)

    if isinstance(geom, (list, tuple)) and len(geom) == 2:
        center, size = geom
        center = np.asarray(center, float)
        size = np.asarray(size, float)
        half_extent = size/2 if size.max() > 5 else size
        return Box(cls, center, half_extent)

    raise TypeError(f"Unrecognised geometry for {key}")

# ───────────────────────────────── Graph builder  ─────────────

def build_scene_graph(boxes: Dict[str, Box]) -> nx.DiGraph:
    G = nx.DiGraph()

    # Nodes
    for key, box in boxes.items():
        G.add_node(key, class_name=box.class_name, id=key, center=box.center.tolist())

    mins, maxs = zip(*(b.aabb for b in boxes.values()))
    room_diag = float(np.linalg.norm(np.max(maxs, 0) - np.min(mins, 0)))

    global a_key, b_key  # used inside relationships()
    keys = list(boxes)
    for i, a_key in enumerate(keys):
        for b_key in keys[i+1:]:
            for u, v, rel in relationships(boxes[a_key], boxes[b_key], room_diag):
                if not G.has_edge(u, v):  # keep first found
                    G.add_edge(u, v, relationship=rel)
    return G

# ───────────────────────── Public convenience API ────────────

def graph_relations(raw_objects: Dict[str, Any]) -> nx.DiGraph:
    boxes = {k: _as_box(k, v) for k, v in raw_objects.items()}
    return build_scene_graph(boxes)
