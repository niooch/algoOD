# Algorytmy Najkrótszych Ścieżek -- Laboratoria 3.

## Cel zadania:

Celem było zaimplementowanie algotytmów znajdowania najkrótszych ścieżek w grafach skierowanych z wagami, wygenerowanych przy użyciu paczki testującej [DIMACS](https://www.diag.uniroma1.it/challenge9/download.shtml). Wszytkie programy stosują się do formatu wejściowego DIMACS.


## Zaimplementowane algorytmy (C++):
1. Algorytm Dijkstry z użyciem priorytetowej kolejki binarnej (standardowa biblioteka C++).
2. Algotytm Diala z C + 1 kubełkami.
3. Algorytm Radix Heap.

## Instrukcja kompilacji i uruchamiania:
Programy można skompilować przy użyciu `make`. Używane są wyłącznie standardowe biblioteki C++.
Odpowiednio dla zadania *single source* 
```bash
./dijkstra -d plik_z_danymi.gr -ss zrodla.ss -oss wyniki.ss.res
./dial -d plik_z_danymi.gr -ss zrodla.ss -oss wyniki.ss.res
./radix_heap -d plik_z_danymi.gr -ss zrodla.ss
```
Oraz dla *pair to pair*:
```bash
./dijkstra -d plik_z_danymi.gr -p2p pary.p2p -op2p wyniki.p2p.res
./dial -d plik_z_danymi.gr -p2p pary.p2p -op2p wyniki.p2p.res
./radix_heap -d plik_z_danymi.gr -p2p pary.p2p -op2p wyniki.p2p.res
```

## Dane 
Dane testowe zostały wygenerowane przy użyciu paczki DIMACS. Znajdują się one w katalogu `inputs/`.
