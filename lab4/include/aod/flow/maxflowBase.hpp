#pragma once
#include <cstdint>
#include <string>

namespace aod {

    struct FlowStats {
        std::int64_t augmentations = 0; //liczba sciezek powiekszajacych przeplyw
        std::int64_t bfs_runs = 0;
        std::int64_t dfs_calls = 0; //Dinic
    };

    class FlowNetwork; 

    class IMaxFlow { //rozne MaxFlow algorytmy
        public:
            virtual ~IMaxFlow() = default;
            virtual std::string name() const = 0;
            virtual long long run(FlowNetwork& net, int s, int t, FlowStats& st) = 0;
    };

} 

