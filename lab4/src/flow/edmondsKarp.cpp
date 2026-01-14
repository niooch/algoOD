#include "aod/flow/edmondsKarp.hpp"
#include "aod/graph/flowNetwork.hpp"  
#include <queue>
#include <vector>
#include <limits>
#include <algorithm>

namespace aod {

    long long EdmondsKarp::run(FlowNetwork& net, int s, int t, FlowStats& st) {
        const int n = net.n();
        auto& g = net.adj();

        long long flow = 0;

        std::vector<int> parent_v(n, -1);
        std::vector<int> parent_e(n, -1);

        auto bfs = [&]() -> bool {
            std::fill(parent_v.begin(), parent_v.end(), -1);
            std::fill(parent_e.begin(), parent_e.end(), -1);

            std::queue<int> q;
            q.push(s);
            parent_v[s] = s;

            while (!q.empty()) {
                int v = q.front();
                q.pop();

                for (int ei = 0; ei < (int)g[v].size(); ++ei) {
                    const Edge& e = g[v][ei];
                    if (parent_v[e.to] != -1) continue;   // już odwiedzony
                    if (e.cap <= 0) continue;             // brak przepustowości w residualu
                    parent_v[e.to] = v;
                    parent_e[e.to] = ei;
                    if (e.to == t) return true;
                    q.push(e.to);
                }
            }
            return parent_v[t] != -1;
        };

        while (bfs()) {
            st.bfs_runs++;

            // bottleneck
            long long add = std::numeric_limits<long long>::max();
            for (int v = t; v != s; v = parent_v[v]) {
                int pv = parent_v[v];
                int ei = parent_e[v];
                add = std::min(add, g[pv][ei].cap);
            }

            // augment
            for (int v = t; v != s; v = parent_v[v]) {
                int pv = parent_v[v];
                int ei = parent_e[v];
                Edge& e = g[pv][ei];
                Edge& rev = g[e.to][e.rev];
                e.cap -= add;
                rev.cap += add;
            }

            flow += add;
            st.augmentations++; // EK: 1 augmentacja = 1 ścieżka powiększająca
        }

        return flow;
    }

} // namespace aod
