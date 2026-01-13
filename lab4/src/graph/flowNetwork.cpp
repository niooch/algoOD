#include "aod/graph/flowNetwork.hpp"

namespace aod {

    void FlowNetwork::add_edge(int u, int v, long long cap) {
        //forward edge
        Edge a;
        a.to = v;
        a.rev = (int)adj_[v].size();
        a.cap = cap;
        a.orig = cap;

        //reverse edge
        Edge b;
        b.to = u;
        b.rev = (int)adj_[u].size();
        b.cap = 0;
        b.orig = 0;

        adj_[u].push_back(a);
        adj_[v].push_back(b);
    }

}

