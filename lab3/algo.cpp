//implementacja algorytmow
#include "algo.h"
#include <queue>    //do generycznego Dijkstry, zlozonosc push: O(log n)
                    //https://en.cppreference.com/w/cpp/container/priority_queue/push.html
//implementacja generycznego Dijkstry z uzyciem kolejki priorytetowej (min-heap)
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

void dial(const Graph& g, int s, std::vector<Distance>& dist, int C){
    int n = static_cast<int>(g.size()-1);
    dist.assign(n+1, INF);
    dist[s] = 0;

    //kubelki
    int binCount = std::max(1, C+1);
    std::vector<std::vector<int>> buckets(binCount);

    int currentBucket = 0;
    buckets[0].push_back(s);

    while(true){
        //znajdz najblizszy niepusty kubelek
        int steps = 0;
        while(buckets[currentBucket].empty() && steps < binCount){
            currentBucket = (currentBucket + 1) % binCount;
            steps++;
        }

        //warunek zakonczenia
        if(steps == binCount && buckets[currentBucket].empty()){
            break; //wszystkie kubelki puste
        }

        int u = buckets[currentBucket].back();
        buckets[currentBucket].pop_back();

        Distance du = dist[u];

        //relaksacja krawedzi
        for(const auto& [v, w] : g[u]){
            Distance dv = dist[v];
            if(du + w < dv){
                dist[v] = du + w;
                int idx = static_cast<int>((du + w) % binCount);
                buckets[idx].push_back(v);
            }
        }
    }
}

void radixheap(const Graph& g, int s, std::vector<Distance>& dist){
    
}
