#!/usr/bin/env python3
import os
from collections import defaultdict


# Rodziny, które chcemy obsłużyć
FAMILIES = [
    "Random4-n",
    "Random4-C",
    "Long-n",
    "Square-n",
    "Long-C",
    "Square-C",
    "USA-road-t",
]


def algo_from_dir(path):
    """
    Z nazwy katalogu (np. 'dijkstraWyniki') robi etykietę algorytmu (np. 'dijkstra').
    """
    name = os.path.basename(os.path.normpath(path))
    for suf in ("Wyniki", "wyniki"):
        if name.endswith(suf):
            name = name[: -len(suf)]
            break
    return name


def parse_n_vertices_from_p2p(path):
    """
    Wyciąga liczbę wierzchołków N z linii:
      g N M Cmin Cmax
    w pliku .p2p.res.
    """
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("g "):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        return int(parts[1])
                    except ValueError:
                        pass
    return None


def parse_p2p_pairs(path):
    """
    Parsuje linie 'd s t dist' z pliku .p2p.res.
    Zwraca listę [(s, t, dist), ...] (typy int).
    """
    pairs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("d "):
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        s = int(parts[1])
                        t = int(parts[2])
                        dist = int(parts[3])
                        pairs.append((s, t, dist))
                    except ValueError:
                        pass
    return pairs


def find_common_instances_for_family(family, results_dirs):
    """
    Dla danej rodziny (np. 'Random4-n') szuka instancji (np. '21.0' albo 'USA')
    dla których istnieje plik .p2p.res w KAŻDYM z katalogów results_dirs.

    Zwraca:
      - listę wspólnych instancji (np. ['21.0', '20.0'])
      - słownik instance -> przykładowa ścieżka .p2p.res (z pierwszego katalogu)
        (przydatne np. do wyznaczenia N).
    """
    prefix = family + "."
    common_instances = None
    sample_paths = {}

    for idx, d in enumerate(results_dirs):
        instances = set()
        for fname in os.listdir(d):
            if not fname.endswith(".p2p.res"):
                continue
            if not fname.startswith(prefix):
                continue
            if "__" not in fname:
                continue

            # wytnij fragment po 'family.' aż do '__'
            rest = fname[len(prefix):]
            inst = rest.split("__", 1)[0]  # np. '21.0' albo 'USA'
            instances.add(inst)

            # zapamiętaj jakąś ścieżkę do tej instancji
            if inst not in sample_paths:
                sample_paths[inst] = os.path.join(d, fname)

        if common_instances is None:
            common_instances = instances
        else:
            common_instances &= instances

    if common_instances is None:
        common_instances = set()

    # odfiltruj sample_paths do wspólnych instancji
    sample_paths = {inst: path for inst, path in sample_paths.items()
                    if inst in common_instances}

    return sorted(common_instances), sample_paths


def instance_size_key(family, instance, sample_path):
    """
    Wyznacza 'rozmiar' instancji do porównywania:
      - dla *-n / *-C: największy wykładnik (np. '21.0' -> 21)
      - dla USA-road-t: liczba wierzchołków N z linii 'g N M ...'
    """
    if family.endswith("-n") or family.endswith("-C"):
        # instancja typu '21.0' -> bierzemy 21
        first = instance.split(".", 1)[0]
        try:
            return int(first)
        except ValueError:
            return -1

    if family == "USA-road-t":
        # używamy N z pliku .p2p.res
        n = parse_n_vertices_from_p2p(sample_path)
        if n is None:
            return -1
        return n

    # domyślnie brak sensownego porządku
    return -1


def build_tables_for_family(family, results_dirs):
    """
    Dla podanej rodziny:
      - znajduje największą wspólną instancję,
      - zbiera wartości dist dla wszystkich algorytmów,
      - wypisuje na stdout fragment LaTeXa z tablicą.
    """
    instances, sample_paths = find_common_instances_for_family(family, results_dirs)
    if not instances:
        print(f"% [WARN] Rodzina {family}: brak wspólnych instancji .p2p.res dla wszystkich algorytmów.\n")
        return

    # wybierz instancję o największym 'rozmiarze'
    best_instance = None
    best_key = None
    for inst in instances:
        key = instance_size_key(family, inst, sample_paths[inst])
        if best_key is None or key > best_key:
            best_key = key
            best_instance = inst

    if best_instance is None:
        print(f"% [WARN] Rodzina {family}: nie udało się wybrać największej instancji.\n")
        return

    # przygotuj listę algów (z katalogów) w podanej kolejności
    algos = [algo_from_dir(d) for d in results_dirs]

    # wczytaj pary z pierwszego katalogu jako kanoniczne
    family_prefix = family + "."
    base = f"{family}.{best_instance}__{family}.{best_instance}.p2p.res"

    # mapowanie algo -> (lista par (s,t,dist), słownik (s,t)->dist)
    data = {}

    for d, algo in zip(results_dirs, algos):
        path = os.path.join(d, base)
        if not os.path.isfile(path):
            print(f"% [WARN] Brak pliku {path} dla algorytmu {algo} – pomijam rodzinę {family}.\n")
            return
        pairs = parse_p2p_pairs(path)
        dist_map = {(s, t): dist for (s, t, dist) in pairs}
        data[algo] = (pairs, dist_map)

    # pary z pierwszego algorytmu
    canonical_algo = algos[0]
    canonical_pairs = data[canonical_algo][0]

    # sprawdzenie zgodności par (opcjonalne, ale przydatne)
    for algo in algos[1:]:
        other_pairs = data[algo][0]
        if len(other_pairs) != len(canonical_pairs):
            print(f"% [WARN] {family}, instancja {best_instance}: różna liczba par w {canonical_algo} i {algo}.")
        # można by sprawdzać dokładniej, ale wystarczy, że odczytamy po (s,t)

    # budowa tabeli LaTeX
    print(f"% =====================================================")
    print(f"% Rodzina {family}, instancja {family}.{best_instance}")
    print(f"% (największa, dla której wszystkie algorytmy mają wynik p2p)")
    print(f"% =====================================================\n")

    # kolumny: para + po jednej kolumnie na każdy algorytm
    col_spec = "cc" + "c" * len(algos)
    print(r"\begin{tabular}{" + col_spec + r"}")
    print(r"\hline")
    header = ["Para $(s,t)$"] + [algo for algo in algos]
    print(" & ".join(header) + r" \\")
    print(r"\hline")

    for (s, t, _) in canonical_pairs:
        row = [rf"$({s},{t})$"]
        for algo in algos:
            dist = data[algo][1].get((s, t))
            if dist is None:
                row.append(r"--")
            else:
                row.append(str(dist))
        print(" & ".join(row) + r" \\")
    print(r"\hline")
    print(r"\end{tabular}")
    print("\n\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Przygotowuje dane do tabelek LaTeX dla największej instancji "
            "każdej rodziny grafów (na podstawie plików .p2p.res)."
        )
    )
    parser.add_argument(
        "results_dirs",
        nargs="+",
        help="Katalogi z wynikami algorytmów (np. dijkstraWyniki dialWyniki radixWyniki)",
    )

    args = parser.parse_args()
    results_dirs = args.results_dirs

    for family in FAMILIES:
        build_tables_for_family(family, results_dirs)


if __name__ == "__main__":
    main()

