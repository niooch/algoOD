#!/usr/bin/env python3
import os
import glob
import random
import sys

# Default directories (can be overridden by arguments if you want)
INPUT_DIR = "inputs"
SS_DIR = "ss"
P2P_DIR = "p2p"


def get_n_from_file(path):
    """
    Parse the .gr file and return n from the 'p sp n m' line.
    """
    with open(path, "r") as f:
        for line in f:
            if line.startswith("p "):
                parts = line.split()
                # Expected: p sp n m
                if len(parts) < 4 or parts[1] != "sp":
                    raise ValueError(f"Unexpected p-line format in {path}: {line.strip()}")
                return int(parts[2])

    raise ValueError(f"No 'p' line found in {path}")


def process_file(path, ss_dir, p2p_dir):
    """
    For a single .gr file:
     1. Create ss/<base>.ss           containing: s 1
     2. Create ss/<base>Rand.ss       containing: 5 random 's nX' lines
     3. Create p2p/<base>.p2p         containing: 5 random 'q nX mX' lines
    """
    base = os.path.basename(path)
    stem, _ = os.path.splitext(base)

    n = get_n_from_file(path)

    os.makedirs(ss_dir, exist_ok=True)
    os.makedirs(p2p_dir, exist_ok=True)

    # 1) ss/<base>.ss with a single line: s 1
    ss_path = os.path.join(ss_dir, f"{stem}.ss")
    with open(ss_path, "w") as f:
        f.write("s 1\n")

    # 2) ss/<base>Rand.ss with 5 random nodes in [1, n]
    rand_ss_path = os.path.join(ss_dir, f"{stem}Rand.ss")
    if n >= 5:
        # Unique nodes
        nodes = random.sample(range(1, n + 1), 5)
    else:
        # Not enough distinct nodes; allow repeats
        nodes = [random.randint(1, n) for _ in range(5)]

    with open(rand_ss_path, "w") as f:
        for v in nodes:
            f.write(f"s {v}\n")

    # 3) p2p/<base>.p2p with 5 random pairs (u, v) in [1, n] x [1, n]
    p2p_path = os.path.join(p2p_dir, f"{stem}.p2p")
    with open(p2p_path, "w") as f:
        for _ in range(5):
            u = random.randint(1, n)
            v = random.randint(1, n)
            f.write(f"q {u} {v}\n")


def main():
    # Optionally allow custom input/ss/p2p dirs via command-line:
    #   python script.py [input_dir] [ss_dir] [p2p_dir]
    input_dir = sys.argv[1] if len(sys.argv) > 1 else INPUT_DIR
    ss_dir = sys.argv[2] if len(sys.argv) > 2 else SS_DIR
    p2p_dir = sys.argv[3] if len(sys.argv) > 3 else P2P_DIR

    pattern = os.path.join(input_dir, "*.gr")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"No .gr files found in '{input_dir}'")
        return

    for path in files:
        process_file(path, ss_dir, p2p_dir)


if __name__ == "__main__":
    main()

