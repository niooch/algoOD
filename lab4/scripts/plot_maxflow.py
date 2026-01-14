#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt


def run_cmd(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def parse_task1_flow(stdout: str):
    lines = [ln.strip() for ln in stdout.splitlines() if ln.strip()]
    if not lines:
        raise ValueError("Empty stdout")
    maxflow = int(lines[0].split()[0])
    edges = []
    for ln in lines[1:]:
        parts = ln.split()
        if len(parts) < 3:
            continue
        u, v, f = int(parts[0]), int(parts[1]), float(parts[2])
        if f > 0:
            edges.append((u, v, f))
    return maxflow, edges


def parse_task2_matching(stdout: str):
    lines = [ln.strip() for ln in stdout.splitlines() if ln.strip()]
    if not lines:
        raise ValueError("Empty stdout")
    matching = int(lines[0].split()[0])
    pairs = []
    for ln in lines[1:]:
        parts = ln.split()
        if len(parts) < 2:
            continue
        u, v = int(parts[0]), int(parts[1])
        pairs.append((u, v))
    return matching, pairs


def compute_layout(G, layout: str, seed: int):
    layout = layout.lower()
    if layout == "spring":
        return nx.spring_layout(G, seed=seed)
    if layout in ("kamada", "kamada_kawai", "kk"):
        return nx.kamada_kawai_layout(G)
    if layout == "circular":
        return nx.circular_layout(G)
    if layout == "spectral":
        return nx.spectral_layout(G)
    if layout == "random":
        return nx.random_layout(G, seed=seed)

    if layout == "graphviz":
        # wymaga pygraphviz lub pydot + graphviz
        try:
            return nx.nx_agraph.graphviz_layout(G, prog="dot")
        except Exception:
            try:
                return nx.nx_pydot.graphviz_layout(G, prog="dot")
            except Exception as e:
                raise RuntimeError("graphviz layout requires pygraphviz or pydot+graphviz") from e

    raise ValueError(f"Unknown layout: {layout}")


def draw_task1(k: int, algo: str, seed: int, bin_task1: str, outdir: Path,
               layout: str, with_labels: bool, max_nodes_labels: int):
    cmd = [bin_task1, "--size", str(k), "--algo", algo, "--seed", str(seed), "--printFlow"]
    code, out, err = run_cmd(cmd)
    if code != 0:
        raise RuntimeError(f"task1 failed\nSTDERR:\n{err}")

    maxflow, edges = parse_task1_flow(out)

    # rysujemy tylko krawędzie z dodatnim przepływem (czytelnie)
    G = nx.DiGraph()
    G.add_nodes_from(range(1 << k))
    for u, v, f in edges:
        G.add_edge(u, v, flow=f)

    pos = compute_layout(G, layout, seed)

    fig = plt.figure(figsize=(10, 7))
    ax = plt.gca()
    ax.set_title(f"Task1: Hypercube k={k} — {algo} — maxflow={maxflow} — seed={seed}")

    # grubości krawędzi proporcjonalne do przepływu (przycięte)
    flows = [G[u][v]["flow"] for u, v in G.edges()]
    if flows:
        mx = max(flows)
        widths = [1.0 + 4.0 * (f / mx) for f in flows]  # 1..5
    else:
        widths = []

    nx.draw_networkx_nodes(G, pos, node_size=200 if (1 << k) <= 64 else 80, ax=ax)
    nx.draw_networkx_edges(G, pos, width=widths, arrows=True, arrowsize=12, ax=ax)

    if with_labels and G.number_of_nodes() <= max_nodes_labels:
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

    ax.axis("off")

    outdir.mkdir(parents=True, exist_ok=True)
    out_path = outdir / f"nx_task1_k{k}_{algo}_seed{seed}_{layout}.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"[task1] wrote {out_path}")


def draw_task2(k: int, degree: int, algo: str, seed: int, bin_task2: str, outdir: Path,
               layout: str, with_labels: bool, max_nodes_labels: int):
    cmd = [bin_task2, "--size", str(k), "--degree", str(degree),
           "--algo", algo, "--seed", str(seed), "--printMatching"]
    code, out, err = run_cmd(cmd)
    if code != 0:
        raise RuntimeError(f"task2 failed\nSTDERR:\n{err}")

    matching, pairs = parse_task2_matching(out)
    m = 1 << k

    # budujemy graf dwudzielny: oznaczamy strony prefiksami
    G = nx.Graph()
    left = [f"L{u}" for u in range(m)]
    right = [f"R{v}" for v in range(m)]
    G.add_nodes_from(left, bipartite=0)
    G.add_nodes_from(right, bipartite=1)

    # dodajemy tylko krawędzie matching (czytelnie)
    for u, v in pairs:
        G.add_edge(f"L{u}", f"R{v}")

    pos = compute_layout(G, layout, seed)

    fig = plt.figure(figsize=(10, 7))
    ax = plt.gca()
    ax.set_title(f"Task2: Matching k={k}, degree={degree} — {algo} — |M|={matching} — seed={seed}")

    # kolorowanie węzłów stronami
    node_colors = []
    for n in G.nodes():
        node_colors.append(0 if n.startswith("L") else 1)

    nx.draw_networkx_nodes(G, pos, node_size=200 if m <= 32 else 80, node_color=node_colors, ax=ax)
    nx.draw_networkx_edges(G, pos, width=2.0, ax=ax)

    if with_labels and G.number_of_nodes() <= max_nodes_labels:
        # krótsze etykiety: bez L/R
        labels = {n: n[1:] for n in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

    ax.axis("off")

    outdir.mkdir(parents=True, exist_ok=True)
    out_path = outdir / f"nx_task2_k{k}_i{degree}_{algo}_seed{seed}_{layout}.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"[task2] wrote {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", type=int, required=True, choices=[1, 2])
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--degree", type=int, default=None, help="required for task2")
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--algo", choices=["ek", "dinic", "both"], default="both")
    ap.add_argument("--layout", default="spring",
                    help="spring|kamada|circular|spectral|random|graphviz (if available)")
    ap.add_argument("--labels", action="store_true", help="draw node labels (only for small graphs)")
    ap.add_argument("--max_labels", type=int, default=80, help="max nodes to draw labels")
    ap.add_argument("--bin_task1", default="./build/task1")
    ap.add_argument("--bin_task2", default="./build/task2")
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    algos = ["ek", "dinic"] if args.algo == "both" else [args.algo]

    if args.task == 1:
        for algo in algos:
            draw_task1(args.k, algo, args.seed, args.bin_task1, outdir,
                       args.layout, args.labels, args.max_labels)
    else:
        if args.degree is None:
            raise SystemExit("--degree is required for task2")
        for algo in algos:
            draw_task2(args.k, args.degree, algo, args.seed, args.bin_task2, outdir,
                       args.layout, args.labels, args.max_labels)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
