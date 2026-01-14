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


def parse_first_int(s: str):
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        # w Twoich taskach stdout zaczyna się od liczby wyniku
        try:
            return int(line.split()[0])
        except Exception:
            pass
    raise ValueError("Cannot parse integer result from stdout")


def parse_glpk_maxflow(stdout: str):
    # w modelu drukujemy: "maxflow %g"
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
    ap.add_argument("--task", type=int, default=1, choices=[1], help="only task1 supported in this simple script")
    ap.add_argument("--kmin", type=int, default=1)
    ap.add_argument("--kmax", type=int, default=12)  # GLPK pliki robią się wielkie — sensownie do ~12
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--bin_task1", default="./build/task1")
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--no_ek", action="store_true", help="skip Edmonds-Karp")
    ap.add_argument("--no_dinic", action="store_true", help="skip Dinic")
    ap.add_argument("--no_glpk", action="store_true", help="skip GLPK")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []

    for k in range(args.kmin, args.kmax + 1):
        for rep in range(args.reps):
            seed = args.seed + k * 1000003 + rep

            # ===== EK =====
            ek_time = None
            ek_val = None
            if not args.no_ek:
                code, out, err, dt = run_cmd([args.bin_task1, "--size", str(k), "--algo", "ek", "--seed", str(seed)])
                if code != 0:
                    print(err)
                    raise SystemExit(f"EK failed (k={k}, rep={rep})")
                ek_val = parse_first_int(out)
                ek_time = dt

            # ===== Dinic =====
            din_time = None
            din_val = None
            if not args.no_dinic:
                code, out, err, dt = run_cmd([args.bin_task1, "--size", str(k), "--algo", "dinic", "--seed", str(seed)])
                if code != 0:
                    print(err)
                    raise SystemExit(f"Dinic failed (k={k}, rep={rep})")
                din_val = parse_first_int(out)
                din_time = dt

            # ===== GLPK =====
            glpk_time = None
            glpk_val = None
            if not args.no_glpk:
                model_path = outdir / f"task1_k{k}_rep{rep}.mod"
                # eksport modelu
                code, out, err, dt_export = run_cmd([args.bin_task1, "--size", str(k), "--seed", str(seed), "--glpk", str(model_path)])
                if code != 0:
                    print(err)
                    raise SystemExit(f"Export failed (k={k}, rep={rep})")

                # solve glpsol (mierzony czas solve + IO)
                code, out, err, dt_solve = run_cmd(["glpsol", "-m", str(model_path)])
                if code != 0:
                    print(err)
                    raise SystemExit(f"glpsol failed (k={k}, rep={rep})")
                glpk_val = parse_glpk_maxflow(out)
                glpk_time = dt_solve

            # sanity: wyniki powinny się zgadzać jeśli liczyliśmy >1 metodą
            vals = [v for v in [ek_val, din_val, glpk_val] if v is not None]
            if vals and any(v != vals[0] for v in vals):
                raise SystemExit(f"Mismatch values for k={k}, rep={rep}: ek={ek_val}, dinic={din_val}, glpk={glpk_val}")

            rows.append({
                "k": k, "rep": rep, "seed": seed,
                "value": vals[0] if vals else None,
                "ek_s": ek_time,
                "dinic_s": din_time,
                "glpk_s": glpk_time,
                })

    df = pd.DataFrame(rows)
    csv_path = outdir / "bench_task1.csv"
    df.to_csv(csv_path, index=False)

    # średnie po k
    g = df.groupby("k", as_index=False).mean(numeric_only=True).sort_values("k")

    fig = plt.figure()
    if "ek_s" in g.columns and g["ek_s"].notna().any():
        plt.plot(g["k"], g["ek_s"], marker="o", label="Edmonds-Karp")
    if "dinic_s" in g.columns and g["dinic_s"].notna().any():
        plt.plot(g["k"], g["dinic_s"], marker="o", label="Dinic")
    if "glpk_s" in g.columns and g["glpk_s"].notna().any():
        plt.plot(g["k"], g["glpk_s"], marker="o", label="GLPK (glpsol)")

    plt.xlabel("k")
    plt.ylabel("time [s]")
    plt.title("Task1: time vs k (avg over reps)")
    plt.legend()

    plt.yscale("log")

    save_plot(fig, outdir / "bench_task1_time_vs_k.png")

    # (opcjonalnie) wykres value vs k
    if "value" in g.columns and g["value"].notna().any():
        fig = plt.figure()
        plt.plot(g["k"], g["value"], marker="o")
        plt.xlabel("k")
        plt.ylabel("maxflow")
        plt.title("Task1: maxflow vs k")
        save_plot(fig, outdir / "bench_task1_value_vs_k.png")

    print(f"Wrote: {csv_path}")
    print(f"Wrote: {outdir / 'bench_task1_time_vs_k.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

