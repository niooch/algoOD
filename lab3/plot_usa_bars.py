#!/usr/bin/env python3
import os
from collections import defaultdict
import matplotlib.pyplot as plt


def parse_res_file(path):
    """
    Parsuje plik .res i zwraca (nazwa_algorytmu, czas_ms).
    """
    algo_name = None
    last_time = None

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("c Algorytm:"):
                algo_name = line.split(":", 1)[1].strip()
            elif line.startswith("t "):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        last_time = float(parts[1])
                    except ValueError:
                        pass

    if algo_name is None:
        algo_name = "unknown"
    if last_time is None:
        raise ValueError(f"Nie znaleziono linii z czasem w pliku {path}")

    return algo_name, last_time


def detect_states(family, results_dirs):
    """
    Wykrywa wszystkie instancje (stany) z plików:
      USA-road-t.<STATE>__USA-road-t.<STATE>...
    """
    states = set()
    prefix = family + "."

    for d in results_dirs:
        for fname in os.listdir(d):
            if not fname.startswith(prefix):
                continue
            if "__" not in fname:
                continue
            middle = fname[len(prefix):].split("__", 1)[0]
            if middle:
                states.add(middle)

    return sorted(states)


def collect_times_all_states(family, states, results_dirs):
    """
    Zbiera czasy dla wszystkich stanów i algorytmów.

    Zwraca dwie struktury:
      times_rand[algo][state] = time_ms
      times_ss[algo][state]   = time_ms
    """
    times_rand = defaultdict(dict)
    times_ss = defaultdict(dict)

    for state in states:
        base = f"{family}.{state}__{family}.{state}"
        rand_suffix = "Rand.ss.res"
        ss_suffix = ".ss.res"

        for d in results_dirs:
            # Rand
            rand_path = os.path.join(d, base + rand_suffix)
            if os.path.isfile(rand_path):
                algo, t_ms = parse_res_file(rand_path)
                times_rand[algo][state] = t_ms

            # zwykłe ss (bez Rand)
            ss_path = os.path.join(d, base + ss_suffix)
            if os.path.isfile(ss_path):
                algo, t_ms = parse_res_file(ss_path)
                times_ss[algo][state] = t_ms

    return times_rand, times_ss


def plot_grouped_bars(times_by_algo, states, title, out_name):
    """
    Rysuje wykres słupkowy z grupami:
      - states na osi X
      - dla każdego algorytmu osobny słupek w grupie.
    """
    if not times_by_algo:
        print(f"Brak danych do wykresu: {out_name}")
        return

    algos = sorted(times_by_algo.keys())
    n_states = len(states)
    n_algos = len(algos)

    # przygotuj dane: jeśli dla jakiegoś alg/stanu brak, ustaw None
    values = {
        algo: [
            times_by_algo[algo].get(state, None)
            for state in states
        ]
        for algo in algos
    }

    x = list(range(n_states))
    total_width = 0.8
    bar_width = total_width / max(n_algos, 1)

    plt.figure()
    for i, algo in enumerate(algos):
        # przesunięcie każdej serii
        offset = -total_width/2 + (i + 0.5) * bar_width
        bar_x = [xi + offset for xi in x]
        ys = values[algo]
        # filtrujemy None – ustawiamy na 0 i niech znikną z logarytmu
        ys_plot = [y if y is not None else 0.0 for y in ys]
        plt.bar(bar_x, ys_plot, width=bar_width, label=algo)

    plt.xticks(x, states, rotation=30, ha="right")
    plt.ylabel("Czas [ms]")
    plt.title(title)
    plt.legend()
    plt.grid(axis="y")

    # oś Y logarytmiczna (duże różnice czasów)
    plt.yscale("log")

    plt.tight_layout()
    plt.savefig(out_name)
    print(f"Zapisano wykres: {out_name}")
    plt.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Wykres słupkowy porównujący algorytmy dla wszystkich "
            "instancji rodziny USA-road-t (osobno Rand i ss)."
        )
    )
    parser.add_argument(
        "results_dirs",
        nargs="+",
        help="Katalogi z wynikami (np. dijkstraWyniki dialWyniki radixWyniki)",
    )

    args = parser.parse_args()

    family = "USA-road-t"
    results_dirs = args.results_dirs

    states = detect_states(family, results_dirs)
    print("Wykryte instancje:", ", ".join(states))

    times_rand, times_ss = collect_times_all_states(family, states, results_dirs)

    # Rand
    title_rand = f"{family}: test Rand (Rand.ss) – wszystkie instancje"
    out_rand = f"{family}_all_states_Rand_bar.png"
    plot_grouped_bars(times_rand, states, title_rand, out_rand)

    # ss
    title_ss = f"{family}: test ss – wszystkie instancje"
    out_ss = f"{family}_all_states_ss_bar.png"
    plot_grouped_bars(times_ss, states, title_ss, out_ss)


if __name__ == "__main__":
    main()
