#include "aod/flow/dinic.hpp"
#include "aod/graph/flowNetwork.hpp"

namespace aod {

    long long Dinic::run(FlowNetwork& net, int s, int t, FlowStats& st) {
        (void)net; (void)s; (void)t;
        st.augmentations = 0;
        st.bfs_runs = 0;
        st.dfs_calls = 0;
        return 0; // na razie stub
    }

} // namespace aod

