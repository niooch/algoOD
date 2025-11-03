import matplotlib.pyplot as plt
import networkx as nx

# --- dane ---
N = 10
s = 1
t = 10
Tmax = 15

# lista łuków (i, j, c, t)
arcs = [
    (1, 2, 3, 4),  (1, 3, 4, 9),  (1, 4, 7, 10), (1, 5, 8, 12),
    (2, 3, 2, 3),  (3, 4, 4, 6),  (3, 5, 2, 2),  (3, 10, 6, 11),
    (4, 5, 1, 1),  (4, 7, 3, 5),  (5, 6, 5, 6),  (5, 7, 3, 3),
    (5, 10, 5, 8), (6, 1, 5, 8),  (6, 7, 2, 2),  (6, 10, 7, 11),
    (7, 3, 4, 6),  (7, 8, 3, 5),  (7, 9, 1, 1),  (8, 9, 1, 2),
    (9, 10, 2, 2),
]

# przykładowa ścieżka spełniająca Tmax=15: 1-2-3-5-7-9-10
feasible_path = [(1,2), (2,3), (3,5), (5,7), (7,9), (9,10)]

# --- budowa grafu skierowanego ---
G = nx.DiGraph()
G.add_nodes_from(range(1, N+1))
for i, j, c, ttime in arcs:
    G.add_edge(i, j, c=c, t=ttime)

# --- pozycje węzłów (możesz zmienić na inną layout'ę) ---
pos = nx.spring_layout(G, seed=7)  # stały seed = powtarzalny rysunek

# --- rysowanie węzłów i krawędzi ---
plt.figure(figsize=(20, 14))
nx.draw_networkx_nodes(G, pos, node_size=900, node_color="#f2f2f2", edgecolors="black")
nx.draw_networkx_labels(G, pos, labels={n: str(n) for n in G.nodes()}, font_size=12)

# krawędzie nie należące do ścieżki
other_edges = [e for e in G.edges() if e not in feasible_path]
nx.draw_networkx_edges(G, pos, edgelist=other_edges, width=1.5, arrowstyle="-|>", arrowsize=16, alpha=0.7)

# krawędzie ścieżki (podświetlone)
nx.draw_networkx_edges(
    G, pos, edgelist=feasible_path, width=3.0, arrowstyle="-|>", arrowsize=20, edge_color="tab:green"
)

# --- etykiety na krawędziach: koszt (c) czerwony, czas (t) niebieski ---
# przygotuj słowniki etykiet
labels_c = {(u, v): f"c={G[u][v]['c']}" for u, v in G.edges()}
labels_t = {(u, v): f"t={G[u][v]['t']}" for u, v in G.edges()}

# narysuj dwa komplety etykiet po dwóch stronach krawędzi
# label_pos=0.35 (bliżej źródła) i 0.65 (bliżej celu) żeby się nie nakładały
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_c, font_color="red", font_size=9, label_pos=0.35, rotate=False)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_t, font_color="blue", font_size=9, label_pos=0.65, rotate=False)

# --- podpis i pokaz ---
plt.title(f"RCSP: s={s}, t={t}, Tmax={Tmax} | Ścieżka zaznaczona na zielono (czas=15, koszt=13)")
plt.axis("off")
plt.tight_layout()
plt.savefig("wlasny.png")

