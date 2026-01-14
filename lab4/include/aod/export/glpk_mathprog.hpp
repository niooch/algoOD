#pragma once
#include <string>

namespace aod {
class FlowNetwork;

void export_maxflow_mathprog(const FlowNetwork& net, int s, int t, const std::string& path);

} // namespace aod

