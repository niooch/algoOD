#include "aod/flow/edmondsKarp.hpp"
#include "aod/graph/flowNetwork.hpp"

namespace aod {

long long EdmondsKarp::run(FlowNetwork& net, int s, int t, FlowStats& st) {
  (void)net; (void)s; (void)t;
  st.augmentations = 0;
  st.bfs_runs = 0;
  return 0; // na razie stub
}

} // namespace aod

