#!/usr/bin/env python3
import os
import glob
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

INPUT_DIR = "inputs"
SS_DIR = "ss"
P2P_DIR = "p2p"

PROGRAMS = [
    "./dijkstra",
    "./dial",
    "./radixheap",
]

OUTPUT_DIRS = {
    "dijkstra": "dijkstraWyniki",
    "dial": "dialWyniki",
    "radixheap": "radixheapWyniki",
}

# Default number of parallel workers (threads)
DEFAULT_WORKERS = 16


def find_tests_for_graph(graph_path):
    """
    For a given inputs/foo.gr, find:
      - all ss/foo*.ss in ss/
      - all p2p/foo*.p2p in p2p/
    """
    stem = Path(graph_path).stem

    ss_tests = sorted(glob.glob(os.path.join(SS_DIR, f"{stem}*.ss")))
    p2p_tests = sorted(glob.glob(os.path.join(P2P_DIR, f"{stem}*.p2p")))

    return ss_tests, p2p_tests


def build_jobs():
    """
    Build a list of all runs to perform.
    Each job is a dict with keys:
    - prog_path, prog_name
    - graph_path
    - test_type ('ss' or 'p2p')
    - test_path
    - out_path
    """
    jobs = []

    graph_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.gr")))
    if not graph_files:
        print(f"No .gr files found in {INPUT_DIR}/")
        return jobs

    for graph_path in graph_files:
        ss_tests, p2p_tests = find_tests_for_graph(graph_path)
        stem = Path(graph_path).stem

        for prog_path in PROGRAMS:
            prog_name = os.path.basename(prog_path).lstrip("./")
            out_dir = OUTPUT_DIRS.get(prog_name, f"{prog_name}Wyniki")
            os.makedirs(out_dir, exist_ok=True)

            # SS tests
            for test_path in ss_tests:
                test_base = Path(test_path).stem  # e.g. foo or fooRand
                out_filename = f"{stem}__{test_base}.ss.res"
                out_path = os.path.join(out_dir, out_filename)

                jobs.append({
                    "prog_path": prog_path,
                    "prog_name": prog_name,
                    "graph_path": graph_path,
                    "test_type": "ss",
                    "test_path": test_path,
                    "out_path": out_path,
                })

            # P2P tests
            for test_path in p2p_tests:
                test_base = Path(test_path).stem
                out_filename = f"{stem}__{test_base}.p2p.res"
                out_path = os.path.join(out_dir, out_filename)

                jobs.append({
                    "prog_path": prog_path,
                    "prog_name": prog_name,
                    "graph_path": graph_path,
                    "test_type": "p2p",
                    "test_path": test_path,
                    "out_path": out_path,
                })

    return jobs


def run_job(job, idx, total):
    prog_path = job["prog_path"]
    prog_name = job["prog_name"]
    graph_path = job["graph_path"]
    test_type = job["test_type"]
    test_path = job["test_path"]
    out_path = job["out_path"]

    graph_stem = Path(graph_path).stem
    test_file = os.path.basename(test_path)

    print(f"[{idx}/{total}] START {prog_name}: {graph_stem} ({test_type}) using {test_file} -> {out_path}")

    if test_type == "ss":
        cmd = [
            prog_path,
            "-d", graph_path,
            "-ss", test_path,
            "-oss", out_path,
        ]
    elif test_type == "p2p":
        cmd = [
            prog_path,
            "-d", graph_path,
            "-p2p", test_path,
            "-op2p", out_path,
        ]
    else:
        raise ValueError(f"Unknown test_type {test_type}")

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print(f"[{idx}/{total}] FAIL {prog_name}: return code {result.returncode}")
    else:
        print(f"[{idx}/{total}] DONE {prog_name}")

    return result.returncode


def main():
    # Optional: first command-line argument = number of workers
    if len(sys.argv) > 1:
        try:
            max_workers = int(sys.argv[1])
        except ValueError:
            print(f"Invalid worker count '{sys.argv[1]}', using default {DEFAULT_WORKERS}")
            max_workers = DEFAULT_WORKERS
    else:
        max_workers = DEFAULT_WORKERS

    jobs = build_jobs()
    if not jobs:
        return

    total = len(jobs)
    print(f"Total runs to perform: {total}")
    print(f"Running with up to {max_workers} parallel workers.\n")

    # Submit jobs to a thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for idx, job in enumerate(jobs, start=1):
            future = executor.submit(run_job, job, idx, total)
            futures[future] = (job, idx)

        # Iterate as jobs finish (for extra status / error reporting)
        for future in as_completed(futures):
            job, idx = futures[future]
            prog_name = job["prog_name"]
            try:
                rc = future.result()
                if rc != 0:
                    print(f"[{idx}/{total}] {prog_name} finished with non-zero exit code: {rc}")
            except Exception as e:
                print(f"[{idx}/{total}] {prog_name} raised an exception: {e}")


if __name__ == "__main__":
    main()
