//struktura oraz dane meta grafu
#pragma once

#include <vector>
#include <string>
#include "common.h"

struct Edge {
    int to; //indeks wierzchołka docelowego
    int w; //waga krawędzi
};

using Graph = std::vector<std::vector<Edge>>;

struct GraphMeta {
    int n; //liczba wierzchołków
    int m; //liczba krawędzi
    int minCost; //minimalny koszt krawędzi
    int maxCost; //maksymalny koszt krawędzi
};

GraphMeta loadGraph(const std::string& path, Graph& graph);
