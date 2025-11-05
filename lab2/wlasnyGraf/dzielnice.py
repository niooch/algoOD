import math
import matplotlib.pyplot as plt
import networkx as nx

# --- dane z zadania ---
a = {1: 10, 2: 20, 3: 18}                 # minima zmian
b = {"p1": 10, "p2": 14, "p3": 13}        # minima dzielnic
L = {
    ("p1", 1): 2, ("p1", 2): 4, ("p1", 3): 3,
    ("p2", 1): 3, ("p2", 2): 6, ("p2", 3): 5,
    ("p3", 1): 5, ("p3", 2): 7, ("p3", 3): 6,
}
U = {
    ("p1", 1): 3,  ("p1", 2): 7,  ("p1", 3): 5,
    ("p2", 1): 5,  ("p2", 2): 7,  ("p2", 3): 10,
    ("p3", 1): 8,  ("p3", 2): 12, ("p3", 3): 10,
}

def fmt_U(uval):
    return "∞" if math.isinf(uval) else str(uval)

# --- sieć cyrkulacji ---
G = nx.DiGraph()
r, t = "r", "t"
S_nodes = [f"S{j}" for j in (1, 2, 3)]
P_nodes = [f"P{i}" for i in (1, 2, 3)]
G.add_nodes_from([r, t] + S_nodes + P_nodes)

for j in (1, 2, 3):
    G.add_edge(r, f"S{j}", L=a[j], U=math.inf, c=1)
for i_name in ("p1", "p2", "p3"):
    i_idx = int(i_name[1])
    for j in (1, 2, 3):
        G.add_edge(f"S{j}", f"P{i_idx}", L=L[(i_name, j)], U=U[(i_name, j)], c=0)
for i_name in ("p1", "p2", "p3"):
    i_idx = int(i_name[1])
    G.add_edge(f"P{i_idx}", t, L=b[i_name], U=math.inf, c=0)
G.add_edge(t, r, L=0, U=math.inf, c=0)

# --- layout warstwowy (proste krawędzie) ---
pos = {r: (0.0, 0.5), t: (3.0, 0.5)}
for k, sj in enumerate(S_nodes, start=1):
    pos[sj] = (1.0, 1.0 - 0.3 * k)
for k, pi in enumerate(P_nodes, start=1):
    pos[pi] = (2.0, 1.0 - 0.3 * k)

# --- rysuj węzły i krawędzie ---
plt.figure(figsize=(12, 6))
node_colors = []
for n in G.nodes():
    if n == r: node_colors.append("#ffd166")
    elif n == t: node_colors.append("#06d6a0")
    elif n.startswith("S"): node_colors.append("#a8dadc")
    else: node_colors.append("#f4a261")

nx.draw_networkx_nodes(G, pos, node_size=1400, node_color=node_colors, edgecolors="black")
nx.draw_networkx_labels(G, pos, font_size=12)

edges_cost_pos = [(u, v) for u, v, d in G.edges(data=True) if d["c"] > 0]
edges_cost_zero = [(u, v) for u, v, d in G.edges(data=True) if d["c"] == 0]

nx.draw_networkx_edges(G, pos, edgelist=edges_cost_zero,
                       width=1.6, alpha=0.9, arrowstyle="-|>", arrowsize=16)
nx.draw_networkx_edges(G, pos, edgelist=edges_cost_pos,
                       width=3.0, edge_color="#e63946", arrowstyle="-|>", arrowsize=20)

# --- funkcje do etykiet równoległych do krawędzi ---
def edge_point(u, v, t_frac=0.5, offset=0.0):
    """punkt na krawędzi (t_frac wzdłuż u->v) z przesunięciem 'offset' prostopadle."""
    x1, y1 = pos[u]; x2, y2 = pos[v]
    mx = x1 + t_frac * (x2 - x1)
    my = y1 + t_frac * (y2 - y1)
    dx, dy = (x2 - x1), (y2 - y1)
    norm = math.hypot(dx, dy)
    if norm == 0:
        return mx, my, 0.0
    # kąty i normalna
    angle_deg = math.degrees(math.atan2(dy, dx))
    nxp, nyp = -dy / norm, dx / norm   # jednostkowa normalna (prostopadle)
    return mx + offset * nxp, my + offset * nyp, angle_deg

def draw_edge_label_parallel(u, v, text, t_frac=0.5, offset=0.02, color="black", size=10):
    x, y, ang = edge_point(u, v, t_frac=t_frac, offset=offset)
    # rotation_mode="anchor" utrzymuje ładne kotwiczenie tekstu
    plt.text(x, y, text, fontsize=size, color=color,
             ha="center", va="center",
             rotation=ang, rotation_mode="anchor")

# --- etykiety: "[L–U] | c=..." (bez tła), równoległe do krawędzi ---
def label_for(u, v, d):
    return f"{d['L']}–{fmt_U(d['U'])} | c={d['c']}"

# Schemat delikatnego „rozgęszczenia”:
# - r->S : czerwone, t_frac=0.45
# - S->P : t_frac zależny od P (0.35, 0.5, 0.65) i offset +/- 0.02
# - P->t : t_frac=0.55
# - t->r : t_frac=0.5
for u, v, d in G.edges(data=True):
    lbl = label_for(u, v, d)
    if u == r and v.startswith("S"):
        draw_edge_label_parallel(u, v, lbl, t_frac=0.45, offset=0.03, color="#e63946", size=10)
    elif u.startswith("S") and v.startswith("P"):
        pi = int(v[1])  # 1..3
        t_pos = {1: 0.35, 2: 0.50, 3: 0.65}[pi]
        off   = {1: +0.02, 2: 0.00, 3: -0.02}[pi]
        draw_edge_label_parallel(u, v, lbl, t_frac=t_pos, offset=off, size=9)
    elif u.startswith("P") and v == t:
        draw_edge_label_parallel(u, v, lbl, t_frac=0.55, offset=0.02, size=9)
    else:  # t->r
        draw_edge_label_parallel(u, v, lbl, t_frac=0.50, offset=0.02, size=9)

plt.title("Cyrkulacja radiowozów")
plt.axis("off")
plt.tight_layout()
plt.savefig("dzielnice.png", dpi=300)
