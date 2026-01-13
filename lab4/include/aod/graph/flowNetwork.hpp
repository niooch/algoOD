#pragma once
#include <vector>
#include <cstdint>

namespace aod {

    struct Edge {
        int to;
        int rev; //index krawędzi odwrotnej w adj[to]
        long long cap; //residual capacity
        long long orig = 0; //oryginalna pojemność
    };

    class FlowNetwork {
        public:
            explicit FlowNetwork(int n = 0) : adj_(n) {}

            int n() const { return (int)adj_.size(); }
            void reset(int n) { adj_.assign(n, {}); }

            void add_edge(int u, int v, long long cap);

            std::vector<std::vector<Edge>>& adj() { return adj_; }
            const std::vector<std::vector<Edge>>& adj() const { return adj_; }

        private:
            std::vector<std::vector<Edge>> adj_;
    };

}

