#include "aod/flow/dinic.hpp"
#include "aod/graph/flowNetwork.hpp" 

#include <vector>
#include <queue>
#include <limits>
#include <algorithm>
#include <functional>

namespace aod {

long long Dinic::run(FlowNetwork& net, int s, int t, FlowStats& st) {
  const int n = net.n();
  auto& g = net.adj();

  std::vector<int> level(n, -1);
  std::vector<int> it(n, 0);

  auto bfs = [&]() -> bool {
    std::fill(level.begin(), level.end(), -1);
    std::queue<int> q;
    level[s] = 0;
    q.push(s);

    while (!q.empty()) {
      int v = q.front();
      q.pop();
      for (const auto& e : g[v]) {
        if (e.cap <= 0) continue;
        if (level[e.to] != -1) continue;
        level[e.to] = level[v] + 1;
        q.push(e.to);
      }
    }
    st.bfs_runs++;
    return level[t] != -1;
  };

  // DFS: pcha przepływ po grafie poziomów
  std::function<long long(int,long long)> dfs = [&](int v, long long pushed) -> long long {
    st.dfs_calls++;
    if (pushed == 0) return 0;
    if (v == t) return pushed;

    for (int& i = it[v]; i < (int)g[v].size(); ++i) {
      Edge& e = g[v][i];
      if (e.cap <= 0) continue;
      if (level[e.to] != level[v] + 1) continue;

      long long tr = dfs(e.to, std::min(pushed, e.cap));
      if (tr == 0) continue;

      e.cap -= tr;
      g[e.to][e.rev].cap += tr;
      st.augmentations++; // policzmy "udane pchnięcie"
      return tr;
    }
    return 0;
  };

  long long flow = 0;
  while (bfs()) {
    std::fill(it.begin(), it.end(), 0);
    while (true) {
      long long pushed = dfs(s, std::numeric_limits<long long>::max());
      if (pushed == 0) break;
      flow += pushed;
    }
  }

  return flow;
}

} // namespace aod
