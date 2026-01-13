#pragma once
#include "aod/graph/flowNetwork.hpp"
#include <vector>
#include <utility>
#include <cstdint>

namespace aod {


    using EdgeRef = std::pair<int,int>;//lista (u, idx) wskazującą na forward-edge w net.adj()[u][idx]

    struct GeneratedFlowInstance {
        FlowNetwork net;
        int s = 0;
        int t = 0;
        std::vector<EdgeRef> forward_edges; //do printFlow / printMatching
    };

    GeneratedFlowInstance generate_hypercube(int k, std::uint64_t seed);
    GeneratedFlowInstance generate_bipartite_matching(int k, int degree, std::uint64_t seed);

} // namespace aod

