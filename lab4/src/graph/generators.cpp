#include "aod/graph/generators.hpp"
#include "aod/rng.hpp"
#include <stdexcept>

namespace aod {

    GeneratedFlowInstance generate_hypercube(int k, std::uint64_t seed) {
        if (k < 1 || k > 30) { // 2^31 to już za dużo na int
            throw std::runtime_error("k out of range");
        }

        const int n = 1 << k;
        (void)seed; // na razie niewykorzystany w stubie

        GeneratedFlowInstance inst;
        inst.net = FlowNetwork(n);
        inst.s = 0;
        inst.t = n - 1;
        // inst.forward_edges zostawiamy puste na razie
        return inst;
    }

    GeneratedFlowInstance generate_bipartite_matching(int k, int degree, std::uint64_t seed) {
        if (k < 1 || k > 30) throw std::runtime_error("k out of range");
        if (degree < 0) throw std::runtime_error("degree must be >= 0");
        (void)seed;

        const int m = 1 << k;
        const int S = 0;
        const int V1_start = 1;
        const int V2_start = 1 + m;
        const int T = 1 + 2 * m;
        const int N = T + 1;

        GeneratedFlowInstance inst;
        inst.net = FlowNetwork(N);
        inst.s = S;
        inst.t = T;
        (void)V1_start; (void)V2_start; (void)degree;
        return inst;
    }

} // namespace aod

