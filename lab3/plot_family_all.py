#!/usr/bin/env python3
import os
import re
from collections import defaultdict

import matplotlib.pyplot as plt


def parse_res_file(path):
    """
    Parsuje plik .res i zwraca (nazwa_algorytmu, czas_ms, n_vertices).

    - nazwa algorytmu: z linii 'c Algorytm: ...'
    - czas: z ostatniej linii 't <liczba>'
    - n_vertices: z linii 'g N M Cmin Cmax'
    """
    algo_name = None
    last_time = None
    n_vertices = None

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("c Algorytm:"):
                algo_name = line.split(":", 1)[1].strip()
            elif line.startswith("g "):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        n_vertices = int(parts[1])
                    except ValueError:
                        pass
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

    return algo_name, last_time, n_vertices


def extract_exponent(family, filename):
    """
    Z nazwy pliku typu:
      Long-C.10.0__Long-C.10.0Rand.ss.res
    wyciąga '10' jako exponent.

    Dla USA-road-* zwróci None i użyjemy innego sposobu.
    """
    if not filename.startswith(family + "."):
        return None

    rest = filename[len(family) + 1 :]  # po 'Long-C.' / 'USA-road-t.'
    m = re.match(r"(\d+)\.", rest)
    if not m:
        return None
    return int(m.group(1))


def exponent_to_x(family, exp):
    """
    Dla rodzin typu:
      *-n  -> n = 2^exp
      *-C  -> C = 4^exp
    Dla innych rodzin zwracamy po prostu exponent.
    """
    if family.endswith("-n"):
        return 2 ** exp
    if family.endswith("-C"):
        return 4 ** exp
    return exp


def collect_data_for_family_in_dir(results_dir, family):
    """
    Zbiera dane dla danej rodziny z JEDNEGO katalogu wyników.

    Zwraca:
      data[kind][algo] = lista (x, time_ms)
    gdzie kind to:
      'rand'   -> pliki zawierające 'Rand.ss'
      'ss'     -> pliki zawierające '.ss.res' ale nie 'Rand.ss'
    """
    data = {
        "rand": defaultdict(list),
        "ss": defaultdict(list),
    }

    for fname in os.listdir(results_dir):
        if not fname.endswith(".res"):
            continue
        if not fname.startswith(family + "."):
            continue
        if ".p2p.res" in fname:
            continue  # ignorujemy p2p

        full_path = os.path.join(results_dir, fname)

        # Rand vs zwykłe ss
        if "Rand.ss" in fname:
            kind = "rand"
        elif ".ss.res" in fname:
            kind = "ss"
        else:
            continue

        # Najpierw spróbuj podejścia z wykładnikiem (Long-*, Random4-*, Square-*)
        exp = extract_exponent(family, fname)

        if exp is not None:
            x_value = exponent_to_x(family, exp)
        else:
            # np. USA-road-t.BAY__USA-road-t.BAYRand.ss.res
            # bierzemy N z linii 'g N M ...' jako X
            algo_name, time_ms, n_vertices = parse_res_file(full_path)
            if n_vertices is None:
                # jeśli z jakiegoś powodu się nie uda, pomijamy plik
                continue
            x_value = n_vertices
            # dane już mamy, więc dodajemy i przechodzimy dalej
            data[kind][algo_name].append((x_value, time_ms))
            continue

        # tu jeśli było exp != None:
        algo_name, time_ms, _ = parse_res_file(full_path)
        data[kind][algo_name].append((x_value, time_ms))

    # sortowanie po X
    for kind in data:
        for algo in data[kind]:
            data[kind][algo].sort(key=lambda pair: pair[0])

    return data


def merge_data(data_list):
    merged = {
        "rand": defaultdict(list),
        "ss": defaultdict(list),
    }

    for data in data_list:
        for kind in merged.keys():
            for algo, points in data[kind].items():
                merged[kind][algo].extend(points)

    # sort + usunięcie duplikatów po X
    for kind in merged:
        for algo in merged[kind]:
            pts = merged[kind][algo]
            pts.sort(key=lambda pair: pair[0])
            unique = []
            last_x = None
            for x, t in pts:
                if last_x is None or x != last_x:
                    unique.append((x, t))
                    last_x = x
            merged[kind][algo] = unique

    return merged


def plot_family(data, family):
    kind_labels = {
        "rand": "ss z losowymi źródłami (Rand.ss)",
        "ss": "ss ze stałym zbiorem źródeł (.ss)",
    }

    for kind in ("rand", "ss"):
        if not data[kind]:
            continue

        plt.figure()
        for algo, points in data[kind].items():
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            plt.plot(xs, ys, marker="o", label=algo)

        plt.xlabel("Rozmiar grafu (liczba wierzchołków lub n/C)")
        plt.ylabel("Czas [ms]")
        title = f"{family}: {kind_labels.get(kind, kind)}"
        plt.title(title)
        plt.legend()
        plt.grid(True)

        # obie osie log
        plt.xscale("log")
        plt.yscale("log")

        plt.tight_layout()
        out_name = f"{family}_{kind}_all_algos.png"
        plt.savefig(out_name)
        print(f"Zapisano wykres: {out_name}")
        plt.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Rysuje wykresy czasu działania wszystkich algorytmów "
            "dla zadanej rodziny grafów (Rand i zwykłe ss osobno)."
        )
    )
    parser.add_argument(
        "family",
        help="Nazwa rodziny (np. Long-C, Long-n, Random4-C, Square-n, USA-road-t, ...)",
    )
    parser.add_argument(
        "results_dirs",
        nargs="+",
        help="Katalogi z wynikami (np. dijkstraWyniki dialWyniki radixWyniki)",
    )

    args = parser.parse_args()

    per_dir_data = []
    for d in args.results_dirs:
        per_dir_data.append(collect_data_for_family_in_dir(d, args.family))

    merged = merge_data(per_dir_data)
    plot_family(merged, args.family)


if __name__ == "__main__":
    main()
