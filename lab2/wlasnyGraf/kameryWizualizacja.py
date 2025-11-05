import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PatchCollection

# --- dane wspólne ---
m, n = 10, 12
containers = [
    (1, 2), (1, 5), (1, 9),
    (2, 1), (2, 4), (2, 7), (2, 11),
    (3, 3), (3, 6), (3, 10),
    (4, 2), (4, 5), (4, 8), (4, 12),
    (5, 1), (5, 4), (5, 7), (5, 9),
    (6, 3), (6, 6), (6, 10),
    (7, 2), (7, 5), (7, 8), (7, 11),
    (8, 1), (8, 4), (8, 7), (8, 12),
    (9, 3), (9, 6), (9, 9),
    (10, 2), (10, 5), (10, 8), (10, 10), (10, 12),
    (5, 11), (6, 12), (9, 11),
]

# rozwiązania z Twojego outputu
k2 = 2
cams_k2 = [(2, 2), (2, 9), (3, 5), (4, 10), (5, 3), (5, 12),
           (6, 7), (7, 9), (8, 2), (9, 5), (9, 12), (10, 9)]

k5 = 5
cams_k5 = [(1, 4), (2, 6), (5, 2), (5, 12), (7, 10), (8, 3), (8, 5), (9, 8)]

def rc_to_xy(r, c):
    """Zamiana (wiersz, kolumna) -> współrzędne rysunkowe. y=0 na górze (wiersz 1 u góry)."""
    x = c - 1
    y = m - r  # odwrócenie żeby wiersz 1 był na górze
    return x, y

def draw_grid(ax):
    # siatka komórek
    for r in range(m):
        for c in range(n):
            ax.add_patch(Rectangle((c, r), 1, 1, fill=False, lw=0.6, edgecolor="#bbbbbb"))
    ax.set_xlim(0, n)
    ax.set_ylim(0, m)
    ax.set_aspect("equal")
    ax.set_xticks([i + 0.5 for i in range(n)])
    ax.set_yticks([i + 0.5 for i in range(m)])
    ax.set_xticklabels(range(1, n + 1))
    ax.set_yticklabels(range(m, 0, -1))  # wiersze od góry
    ax.grid(False)
    ax.invert_yaxis()  # tak, by wierzch był na górze

def draw_containers(ax, containers):
    patches = []
    for (r, c) in containers:
        x, y = rc_to_xy(r, c)
        rect = Rectangle((x, y), 1, 1, facecolor="#ffcccc", edgecolor="#cc0000", lw=1.2)
        patches.append(rect)
    pc = PatchCollection(patches, match_original=True)
    ax.add_collection(pc)
    # X na kontenerze
    for (r, c) in containers:
        x, y = rc_to_xy(r, c)
        ax.plot([x + 0.2, x + 0.8], [y + 0.2, y + 0.8], color="#aa0000", lw=1.2)
        ax.plot([x + 0.8, x + 0.2], [y + 0.2, y + 0.8], color="#aa0000", lw=1.2)

def draw_coverage(ax, cameras, k, color="#5dade2", alpha=0.12):
    """Zasięg w krzyżu: poziom i pion do k pól."""
    for (r, c) in cameras:
        # poziom: od max(c-k,1) do min(c+k,n), bez samego pola
        for dc in range(-k, k + 1):
            if dc == 0:
                continue
            c2 = c + dc
            if 1 <= c2 <= n:
                x, y = rc_to_xy(r, c2)
                ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor=None, alpha=alpha))
        # pion:
        for dr in range(-k, k + 1):
            if dr == 0:
                continue
            r2 = r + dr
            if 1 <= r2 <= m:
                x, y = rc_to_xy(r2, c)
                ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor=None, alpha=alpha))

def draw_cameras(ax, cameras, color="#1f77b4", label_prefix="Cam"):
    for idx, (r, c) in enumerate(cameras, start=1):
        x, y = rc_to_xy(r, c)
        # kółko w środku komórki
        circ = Circle((x + 0.5, y + 0.5), 0.28, facecolor=color, edgecolor="black", lw=0.8)
        ax.add_patch(circ)
        # podpis
        ax.text(x + 0.5, y + 0.5, f"{label_prefix}{idx}",
                ha="center", va="center", color="white", fontsize=9, weight="bold")

def visualize(cams, k, ax, title):
    draw_grid(ax)
    draw_containers(ax, containers)
    draw_coverage(ax, cams, k, color="#4da3ff", alpha=0.18)
    draw_cameras(ax, cams, color="#1f77b4", label_prefix="K")
    ax.set_title(f"{title}\n(k={k}, #kamer={len(cams)})")

def main():
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    visualize(cams_k2, k2, axes[0], "Rozwiązanie dla k=2")
    visualize(cams_k5, k5, axes[1], "Rozwiązanie dla k=5")
    plt.tight_layout()
    plt.savefig("kameryWizualizacja.png", dpi=600)

if __name__ == "__main__":
    main()

