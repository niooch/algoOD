#!/usr/bin/env python3
import argparse
import subprocess
import time
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def run_cmd(cmd):
    t0 = time.perf_counter()
    p = subprocess.run(cmd, capture_output=True, text=True)
    t1 = time.perf_counter()
    return p.returncode, p.stdout, p.stderr, (t1 - t0)


def parse_first_int(stdout: str) -> int:
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        return int(line.split()[0])
    raise ValueError("Cannot parse integer from stdout")


def parse_glpk_maxflow(stdout: str) -> int:
    # exporter prints: "maxflow %g"
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("maxflow"):
            val = float(line.split()[1])
            return int(round(val))
    raise ValueError("Cannot find 'maxflow' in glpsol stdout")


def save_plot(fig, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kmin", type=int, default=3)
    ap.add_argument("--kmax", type=int, default=10)
    ap.add_argument("--imin", type=int, default=1, help="min degree i")
    ap.add_argument("--imax", type=int, default=None, help="max degree i (default: i=k)")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--bin_task2", default="./build/task2")
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--no_ek", action="store_true")
    ap.add_argument("--no_dinic", action="store_true")
    ap.add_argument("--no_glpk", action="store_true")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []

    for k in range(args.kmin, args.kmax + 1):
        local_imax = args.imax if args.imax is not None else k  # typowo i<=k
        for deg in range(args.imin, local_imax + 1):
            for rep in range(args.reps):
                seed = args.seed + k * 1000003 + deg * 10007 + rep

                ek_time = None
                ek_val = None
                if not args.no_ek:
                    code, out, err, dt = run_cmd([
                        args.bin_task2, "--size", str(k), "--degree", str(deg),
                        "--algo", "ek", "--seed", str(seed)
                        ])
                    if code != 0:
                        print("=== EK STDERR ===")
                        print(err)
                        raise SystemExit(f"EK failed (k={k}, i={deg}, rep={rep})")
                    ek_val = parse_first_int(out)
                    ek_time = dt

                din_time = None
                din_val = None
                if not args.no_dinic:
                    code, out, err, dt = run_cmd([
                        args.bin_task2, "--size", str(k), "--degree", str(deg),
                        "--algo", "dinic", "--seed", str(seed)
                        ])
                    if code != 0:
                        print("=== Dinic STDERR ===")
                        print(err)
                        raise SystemExit(f"Dinic failed (k={k}, i={deg}, rep={rep})")
                    din_val = parse_first_int(out)
                    din_time = dt

                glpk_time = None
                glpk_val = None
                if not args.no_glpk:
                    model_path = outdir / f"task2_k{k}_i{deg}_rep{rep}.mod"
                    # export
                    code, out, err, dt_export = run_cmd([
                        args.bin_task2, "--size", str(k), "--degree", str(deg),
                        "--seed", str(seed), "--glpk", str(model_path)
                        ])
                    if code != 0:
                        print("=== Export STDERR ===")
                        print(err)
                        raise SystemExit(f"Export failed (k={k}, i={deg}, rep={rep})")

                    # solve
                    code, out, err, dt_solve = run_cmd(["glpsol", "-m", str(model_path)])
                    if code != 0:
                        print("=== glpsol STDOUT ===")
                        print(out)
                        print("=== glpsol STDERR ===")
                        print(err)
                        raise SystemExit(f"glpsol failed (k={k}, i={deg}, rep={rep})")
                    glpk_val = parse_glpk_maxflow(out)
                    glpk_time = dt_solve

                # sanity: wszystkie policzone wartości muszą się zgadzać
                vals = [v for v in [ek_val, din_val, glpk_val] if v is not None]
                if vals and any(v != vals[0] for v in vals):
                    raise SystemExit(
                            f"Mismatch values k={k} i={deg} rep={rep}: ek={ek_val} dinic={din_val} glpk={glpk_val}"
                            )

                rows.append({
                    "k": k, "i": deg, "rep": rep, "seed": seed,
                    "matching": vals[0] if vals else None,
                    "ek_s": ek_time,
                    "dinic_s": din_time,
                    "glpk_s": glpk_time
                    })

    df = pd.DataFrame(rows)
    csv_path = outdir / "bench_task2.csv"
    df.to_csv(csv_path, index=False)

    # === Wykres 1: time vs k dla każdego i (osobne linie), log Y ===
    # Uśrednij po rep
    g_ki = df.groupby(["k", "i"], as_index=False).mean(numeric_only=True).sort_values(["k", "i"])

    # Żeby nie było gigantycznie: rysujemy osobno dla metod, a linie to różne i
    def plot_time_vs_k(method_col: str, title: str, out_name: str):
        if method_col not in g_ki.columns or not g_ki[method_col].notna().any():
            return
        fig = plt.figure()
        for i_val, sub in g_ki.groupby("i"):
            plt.plot(sub["k"], sub[method_col], marker="o", label=f"i={int(i_val)}")
        plt.xlabel("k")
        plt.ylabel("time [s]")
        plt.yscale("log")  # LOG skala czasu
        plt.title(title)
        plt.legend(ncol=2, fontsize=8)
        save_plot(fig, outdir / out_name)

    plot_time_vs_k("ek_s",    "Task2: EK time vs k (lines: degree i)",    "bench_task2_ek_time_vs_k_log.png")
    plot_time_vs_k("dinic_s", "Task2: Dinic time vs k (lines: degree i)", "bench_task2_dinic_time_vs_k_log.png")
    plot_time_vs_k("glpk_s",  "Task2: GLPK time vs k (lines: degree i)",  "bench_task2_glpk_time_vs_k_log.png")

    # === Wykres 2: time vs i (średnio po k i rep), log Y ===
    g_i = df.groupby("i", as_index=False).mean(numeric_only=True).sort_values("i")

    fig = plt.figure()
    if "ek_s" in g_i.columns and g_i["ek_s"].notna().any():
        plt.plot(g_i["i"], g_i["ek_s"], marker="o", label="Edmonds-Karp")
    if "dinic_s" in g_i.columns and g_i["dinic_s"].notna().any():
        plt.plot(g_i["i"], g_i["dinic_s"], marker="o", label="Dinic")
    if "glpk_s" in g_i.columns and g_i["glpk_s"].notna().any():
        plt.plot(g_i["i"], g_i["glpk_s"], marker="o", label="GLPK (glpsol)")
    plt.xlabel("i (degree)")
    plt.ylabel("time [s]")
    plt.yscale("log")  # LOG
    plt.title("Task2: time vs degree i (avg over k,rep)")
    plt.legend()
    save_plot(fig, outdir / "bench_task2_time_vs_i_log.png")

    # === (Opcjonalnie) matching vs i dla każdego k ===
    if "matching" in g_ki.columns and g_ki["matching"].notna().any():
        fig = plt.figure()
        for k_val, sub in g_ki.groupby("k"):
            plt.plot(sub["i"], sub["matching"], marker="o", label=f"k={int(k_val)}")
        plt.xlabel("i (degree)")
        plt.ylabel("matching")
        plt.title("Task2: matching vs i (lines: k)")
        plt.legend(ncol=2, fontsize=8)
        save_plot(fig, outdir / "bench_task2_matching_vs_i.png")

    print(f"Wrote: {csv_path}")
    print(f"Wrote PNGs to: {outdir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

