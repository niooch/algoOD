//implementacja algorytmow
#include "algo.h"
#include <vector>
#include <utility>
#include <cassert>
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

template <class Key>
struct RadixHeap {
    using U = unsigned long long; // internal unsigned type

    // each bucket holds pairs (key, vertex)
    std::vector<std::pair<U,int>> buckets[65];
    U last;           // last popped minimum key
    std::size_t sz;   // number of elements

    RadixHeap() : last(0), sz(0) {}

    bool empty() const { return sz == 0; }
    std::size_t size() const { return sz; }

    // keys must be pushed in non-decreasing order of true distance in Dijkstra
    void push(Key key, int v) {
        U x = static_cast<U>(key);
        // Dijkstra with non-negative weights ensures x >= last
        assert(x >= last);

        int b = bucket_index(x);
        buckets[b].emplace_back(x, v);
        ++sz;
    }

    std::pair<Key,int> top() {
        if (buckets[0].empty()) pull();
        const auto &p = buckets[0].back();
        return { static_cast<Key>(p.first), p.second };
    }

    void pop() {
        if (buckets[0].empty()) pull();
        buckets[0].pop_back();
        --sz;
    }

private:
    // bucket index for key x (given that x >= last)
    int bucket_index(U x) const {
        if (x == last) return 0;
        U diff = x ^ last;
        // msb position in [0..63]
        int msb = 63 - __builtin_clzll(diff);
        return msb + 1; // bucket 1..64
    }

    // move elements from some non-empty bucket i>0 into lower buckets,
    // updating `last` to the new minimum key
    void pull() {
        int i = 1;
        while (i < 65 && buckets[i].empty()) ++i;
        assert(i < 65); // must find a non-empty bucket if sz > 0

        // find new minimum key in bucket i
        U new_last = buckets[i][0].first;
        for (auto &p : buckets[i]) {
            if (p.first < new_last) new_last = p.first;
        }
        last = new_last;

        // re-bucket all elements from bucket i
        for (auto &p : buckets[i]) {
            int b = bucket_index(p.first);
            buckets[b].push_back(p);
        }
        buckets[i].clear();
    }
};

void radixheap(const Graph& g, int s, std::vector<Distance>& dist) {
    int n = static_cast<int>(g.size() - 1);
    dist.assign(n + 1, INF);
    dist[s] = 0;

    RadixHeap<Distance> pq;
    pq.push(0, s);

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue; // stale entry

        for (const auto& [v, w] : g[u]) {
            // assuming w >= 0
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push(dist[v], v);
            }
        }
    }
}

