# AOD Lab 4 — Max Flow, Matching, GLPK

Projekt do laboratorium 4: maksymalny przepływ (Edmonds–Karp + Dinic), skojarzenia w grafie dwudzielnym przez max-flow, benchmarki oraz opcjonalnie eksport modelu do GLPK (MathProg).

## Wymagania

- Kompilator C++17 (np. `g++`)
- `make`
- Python 3 + pakiety: `pandas`, `matplotlib` (do wykresów)
- GLPK: `glpsol`

## Budowanie

```bash
make
```

Binarki pojawią się w `build/`:
- `build/task1` — Zadanie 1 (hiperkostka + maxflow)
- `build/task2` — Zadanie 2 (matching przez maxflow)
- `build/task4` — porównanie algorytmów na tej samej instancji (EK vs Dinic)

## Zadanie 1 — Hiperkostka i max flow

### Uruchomienie
```bash
./build/task1 --size k --algo ek|dinic [--seed X] [--printFlow] [--glpk path.mod]
```

- `--size k` — wymiar hiperkostki (1..16)
- `--algo ek|dinic` — wybór algorytmu
- `--seed X` — powtarzalność losowania (domyślnie: seed z czasu)
- `--printFlow` — wypisuje przepływ na łukach (format: `u v f`)
- `--glpk path.mod` — eksportuje model (MathProg) do GLPK i kończy (Zad.3)

### Wyjście
- **stdout**: wartość maxflow (1 linia), a przy `--printFlow` kolejne linie `u v flow`
- **stderr**: czas działania (ms); dla EK dodatkowo liczba ścieżek powiększających

Przykład:
```bash
./build/task1 --size 8 --algo dinic --seed 123
```

## Zadanie 2 — Maksymalne skojarzenie (matching) przez max flow

### Uruchomienie
```bash
./build/task2 --size k --degree i --algo ek|dinic [--seed X] [--printMatching] [--glpk path.mod]
```

- `--size k` — rozmiar stron: |V1|=|V2|=2^k
- `--degree i` — każdy wierzchołek w V1 ma dokładnie `i` sąsiadów w V2
- `--printMatching` — wypisuje pary `(u v)` w skojarzeniu
- `--glpk path.mod` — eksport modelu max-flow do GLPK (Zad.3)

### Wyjście
- **stdout**: rozmiar matching (1 linia), a przy `--printMatching` kolejne linie `u v`
- **stderr**: czas działania (ms)

Przykład:
```bash
./build/task2 --size 8 --degree 4 --algo dinic --seed 123
```

## Zadanie 3 — GLPK (MathProg)

### Eksport modelu
Przykład (Task1):
```bash
./build/task1 --size 6 --seed 123 --glpk results/t1_k6.mod
glpsol -m results/t1_k6.mod
```

Przykład (Task2):
```bash
./build/task2 --size 6 --degree 3 --seed 123 --glpk results/t2_k6_i3.mod
glpsol -m results/t2_k6_i3.mod
```

Wynik GLPK wypisuje m.in. linię:
```
maxflow <wartość>
```

> Uwaga: dla dużych `k` pliki `.mod` robią się bardzo duże. GLPK warto benchmarkować dla mniejszych zakresów (np. do k≈10–12).

## Porównanie algorytmów (EK vs Dinic)

### Benchmark na tej samej instancji (CSV)
Task1, k=1..16:
```bash
./build/task4_bench --task 1 --kmin 1 --kmax 16 --reps 5 --seed 123 > results/task1_compare.csv
```

Task2, k=3..10 i i=1..k:
```bash
./build/task4_bench --task 2 --kmin 3 --kmax 10 --reps 3 --seed 123 > results/task2_compare.csv
```
