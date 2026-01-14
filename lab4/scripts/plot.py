#!/usr/bin/env python3
import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def save_plot(fig, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_task1(df: pd.DataFrame, outdir: Path, stem: str):
    # grupujemy po k (uśredniamy po rep)
    g = df.groupby("k", as_index=False).mean(numeric_only=True).sort_values("k")

    # czasy
    fig = plt.figure()
    if "ek_us" in g.columns:
        plt.plot(g["k"], g["ek_us"], marker="o", label="ek_us")
    if "dinic_us" in g.columns:
        plt.plot(g["k"], g["dinic_us"], marker="o", label="dinic_us")
    plt.xlabel("k")
    plt.ylabel("time [us]")
    plt.title("Task1: time vs k")
    plt.legend()
    save_plot(fig, outdir / f"{stem}_task1_time_vs_k.png")

    # flow
    if "flow" in g.columns:
        fig = plt.figure()
        plt.plot(g["k"], g["flow"], marker="o")
        plt.xlabel("k")
        plt.ylabel("flow")
        plt.title("Task1: maxflow vs k")
        save_plot(fig, outdir / f"{stem}_task1_flow_vs_k.png")

    # augmentacje EK (jeśli są)
    if "ek_aug" in g.columns:
        fig = plt.figure()
        plt.plot(g["k"], g["ek_aug"], marker="o")
        plt.xlabel("k")
        plt.ylabel("augmentations")
        plt.title("Task1: EK augmentations vs k")
        save_plot(fig, outdir / f"{stem}_task1_ek_aug_vs_k.png")

    # statystyki Dinica (jeśli są)
    for col in ["dinic_bfs", "dinic_dfs", "dinic_aug"]:
        if col in g.columns:
            fig = plt.figure()
            plt.plot(g["k"], g[col], marker="o")
            plt.xlabel("k")
            plt.ylabel(col)
            plt.title(f"Task1: {col} vs k")
            save_plot(fig, outdir / f"{stem}_task1_{col}_vs_k.png")


def plot_task2(df: pd.DataFrame, outdir: Path, stem: str):
    # średnie po (k,i)
    gi = df.groupby(["k", "i"], as_index=False).mean(numeric_only=True).sort_values(["k", "i"])

    # 1) dla każdego k: matching vs i (linie)
    if "matching" in gi.columns:
        fig = plt.figure()
        for k, sub in gi.groupby("k"):
            plt.plot(sub["i"], sub["matching"], marker="o", label=f"k={int(k)}")
        plt.xlabel("i (degree)")
        plt.ylabel("matching")
        plt.title("Task2: matching vs i (for each k)")
        plt.legend(ncol=2, fontsize=8)
        save_plot(fig, outdir / f"{stem}_task2_matching_vs_i_lines.png")

    # 2) czas vs i (osobno EK i Dinic) – uśrednione po k (czyli trend względem stopnia)
    g_i = df.groupby("i", as_index=False).mean(numeric_only=True).sort_values("i")

    fig = plt.figure()
    if "ek_us" in g_i.columns:
        plt.plot(g_i["i"], g_i["ek_us"], marker="o", label="ek_us")
    if "dinic_us" in g_i.columns:
        plt.plot(g_i["i"], g_i["dinic_us"], marker="o", label="dinic_us")
    plt.xlabel("i (degree)")
    plt.ylabel("time [us]")
    plt.title("Task2: time vs i (avg over k)")
    plt.legend()
    save_plot(fig, outdir / f"{stem}_task2_time_vs_i.png")

    # 3) czas vs k dla ustalonego i (jeśli chcesz: dla każdego i osobny wykres)
    if "dinic_us" in df.columns or "ek_us" in df.columns:
        for i_val, sub in df.groupby("i"):
            gk = sub.groupby("k", as_index=False).mean(numeric_only=True).sort_values("k")
            fig = plt.figure()
            if "ek_us" in gk.columns:
                plt.plot(gk["k"], gk["ek_us"], marker="o", label="ek_us")
            if "dinic_us" in gk.columns:
                plt.plot(gk["k"], gk["dinic_us"], marker="o", label="dinic_us")
            plt.xlabel("k")
            plt.ylabel("time [us]")
            plt.title(f"Task2: time vs k (i={int(i_val)})")
            plt.legend()
            save_plot(fig, outdir / f"{stem}_task2_time_vs_k_i{i_val}.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="CSV from task4_bench")
    ap.add_argument("--outdir", default="results", help="output directory for PNGs (default: results)")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    outdir = Path(args.outdir)
    stem = csv_path.stem

    df = pd.read_csv(csv_path)

    # autodetekcja tasku
    cols = set(df.columns)
    if "task" in cols:
        # jeśli w CSV jest task mieszany, rozdziel
        for task_id, sub in df.groupby("task"):
            if int(task_id) == 1:
                plot_task1(sub, outdir, f"{stem}_t1")
            elif int(task_id) == 2:
                plot_task2(sub, outdir, f"{stem}_t2")
        return 0

    # fallback: po kolumnach
    if "i" in cols:
        plot_task2(df, outdir, stem)
    else:
        plot_task1(df, outdir, stem)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
