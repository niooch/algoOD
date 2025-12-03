//kod do zaczytywania grafu z pliku
#include "graph.h"
#include <fstream>
#include <stdexcept>
#include <iostream>

GraphMeta loadGraph(const std::string& path, Graph& graph) {
    std::ifstream in(path);
    if (!in) {
        throw std::runtime_error("Nie moge otworzyc pliku: " + path);
    }

    GraphMeta meta;
    std::string token;

    bool allocated = false;
    int minCost = std::numeric_limits<int>::max();
    int maxCost = 0;

    while (in >> token){
        if (token == "c"){ //komentarz
            std::string commentLine;
            std::getline(in, commentLine); //pomin reszte linii
        } else if (token == "p"){ //definicja problemu > p sp n m 
            std::string problemString;
            in >> problemString >> meta.n >> meta.m;
            if(!in){
                throw std::runtime_error("Blad podczas czytania definicji problemu");
            }
            graph.assign(meta.n+1, {});
            allocated = true;
        } else if (token == "a"){ //krawedz > a u v c
            if(!allocated){
                throw std::runtime_error("Krawedz zdefiniowana przed definicja problemu");
            }
            int u, v, cost;
            in >> u >> v >> cost;
            if(!in){
                throw std::runtime_error("Blad podczas czytania krawedzi");
            }
            if(u<1 || u>meta.n || v<1 || v>meta.n){
                throw std::runtime_error("Nieprawidlowy numer wierzcholka w krawedzi: " + std::to_string(u) + " " + std::to_string(v));
            }
            graph[u].push_back({v, cost});
            if(cost < minCost) minCost = cost;
            if(cost > maxCost) maxCost = cost;
        } else {
            throw std::runtime_error("Nieznany token w pliku: " + token);
        }
    }

    if (!allocated){
        throw std::runtime_error("Brak definicji problemu w pliku");
    }

    meta.minCost = (meta.m > 0 ? minCost : 0);
    meta.maxCost = maxCost;
    return meta;
}
