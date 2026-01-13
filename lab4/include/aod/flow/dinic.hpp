#pragma once
#include "aod/flow/maxflowBase.hpp"

namespace aod {
    class Dinic : public IMaxFlow {
        public:
            std::string name() const override { return "dinic"; }
            long long run(FlowNetwork& net, int s, int t, FlowStats& st) override;
    };
}

