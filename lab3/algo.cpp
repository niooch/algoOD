//implementacja algorytmow
#include "algo.h"
#include <iostream>
#include <queue>    //do generycznego Dijkstry, zlozonosc push: O(log n)
                    //https://en.cppreference.com/w/cpp/container/priority_queue/push.html

void dijkstra(const Graph& g, int s, std::vector<Distance>& dist){
    int n = static_cast<int>(g.size()-1);
    dist.assign(n+1, INF);
    dist[s] = 0;

    using P = std::pair<Distance, int>; //para (odleglosc, wierzcholek)
    std::priority_queue<P, std::vector<P>, std::greater<P>> pq;
    pq.push({0, s});

    while(!pq.empty()){
        auto [d, u] = pq.top();
        pq.pop();
        if(d > dist[u]) continue; //stary wpis w kolejce

        for(const auto& [v, w] : g[u]){
            if(dist[u] + w < dist[v]){
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
}

