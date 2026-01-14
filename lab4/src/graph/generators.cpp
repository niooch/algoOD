#include "aod/graph/generators.hpp"
#include "aod/rng.hpp"
#include <stdexcept>
#include <cstdint>
#include <algorithm>
#include <unordered_set>

namespace aod {

    static inline int popcount_u32(std::uint32_t x) {
        return __builtin_popcount(x);
    }

    GeneratedFlowInstance generate_hypercube(int k, std::uint64_t seed) {
        if (k < 1 || k > 16) {
            throw std::runtime_error("k out of range (expected 1..16)");
        }

        const int n = 1 << k;

        GeneratedFlowInstance inst;
        inst.net = FlowNetwork(n);
        inst.s = 0;
        inst.t = n - 1;
        inst.forward_edges.clear();
        inst.forward_edges.reserve((std::size_t)k * (std::size_t)(1u << (k - 1)));

        // (opcjonalnie) przyspieszenie: typowo ~k wyjść + reverse edges, więc rezerwujemy trochę
        for (int v = 0; v < n; ++v) inst.net.adj()[v].reserve((std::size_t)2 * (std::size_t)k);

        RNG rng(seed);

        for (int i = 0; i < n; ++i) {
            const int Hi = popcount_u32((std::uint32_t)i);
            const int Zi = k - Hi;

            for (int b = 0; b < k; ++b) {
                if ((i & (1 << b)) != 0) continue; // bit=1 -> nie ma "w górę" tym bitem

                const int j = i | (1 << b);

                // Dla j: Hamming rośnie o 1, liczba zer maleje o 1
                const int Hj = Hi + 1;
                const int Zj = Zi - 1;

                const int l = std::max({Hi, Zi, Hj, Zj});
                const long long cap_max = 1LL << l;        // 2^l
                const long long cap = rng.uniform_ll(1, cap_max);

                inst.net.add_edge(i, j, cap);

                // zapisz referencję do właśnie dodanej krawędzi forward
                int idx = (int)inst.net.adj()[i].size() - 1;
                inst.forward_edges.push_back({i, idx});
            }
        }

        return inst;
    }

    GeneratedFlowInstance generate_bipartite_matching(int k, int degree, std::uint64_t seed) {
        if (k < 1 || k > 16) throw std::runtime_error("k out of range (expected 1..16 for labs)");
        const int m = 1 << k;                 // |V1|=|V2|=2^k
        if (degree < 0) throw std::runtime_error("degree must be >= 0");
        if (degree > m) throw std::runtime_error("degree > |V2| would force duplicates / infinite loop");

        // Układ wierzchołków w sieci:
        // S=0
        // V1: [1 .. m]
        // V2: [1+m .. 2m]
        // T = 1+2m
        const int S = 0;
        const int V1_start = 1;
        const int V2_start = 1 + m;
        const int T = 1 + 2 * m;
        const int N = T + 1;

        GeneratedFlowInstance inst;
        inst.net = FlowNetwork(N);
        inst.s = S;
        inst.t = T;
        inst.forward_edges.clear();
        inst.forward_edges.reserve((std::size_t)m * (std::size_t)degree);

        // Rezerwy (opcjonalnie, ale pomaga)
        inst.net.adj()[S].reserve((std::size_t)m);
        inst.net.adj()[T].reserve((std::size_t)m);
        for (int u = 0; u < m; ++u) {
            inst.net.adj()[V1_start + u].reserve((std::size_t)(degree + 1) * 2);
            inst.net.adj()[V2_start + u].reserve((std::size_t)2 * 2);
        }

        RNG rng(seed);

        // S -> V1 (cap 1)
        for (int u = 0; u < m; ++u) {
            inst.net.add_edge(S, V1_start + u, 1);
        }

        // V2 -> T (cap 1)
        for (int v = 0; v < m; ++v) {
            inst.net.add_edge(V2_start + v, T, 1);
        }

        // V1 -> V2 (cap 1), dokładnie 'degree' unikalnych sąsiadów na każdy u
        for (int u = 0; u < m; ++u) {
            std::unordered_set<int> chosen;
            chosen.reserve((std::size_t)degree * 2);

            while ((int)chosen.size() < degree) {
                int v = rng.uniform_int(0, m - 1);
                chosen.insert(v);
            }

            int nu = V1_start + u;
            for (int v : chosen) {
                int nv = V2_start + v;
                inst.net.add_edge(nu, nv, 1);

                // referencja do właśnie dodanej forward-krawędzi nu -> nv
                int idx = (int)inst.net.adj()[nu].size() - 1;
                inst.forward_edges.push_back({nu, idx});
            }
        }

        return inst;
    }

} // namespace aod
