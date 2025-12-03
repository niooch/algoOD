//algorytmy wyznaczania najkrotszej sciezki w grafie
#pragma once
#include <vector>
#include <array>
#include <stdexcept>
#include "common.h"
#include "graph.h"

void dijkstra(const Graph& graph, int s, std::vector<Distance>& dist);
void dial(const Graph& g, int s, std::vector<Distance>& dist, int C);
void radixheap(const Graph& g, int s, std::vector<Distance>& dist);

