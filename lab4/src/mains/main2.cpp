#include "aod/timer.hpp"
#include "aod/graph/generators.hpp"
#include "aod/flow/edmondsKarp.hpp"
#include "aod/flow/dinic.hpp"
#include <iostream>
#include <string>
#include <cstdint>

static int require_int(int& i, int argc, char** argv) {
    if (i + 1 >= argc) { std::cerr << "Missing value after " << argv[i] << "\n"; std::exit(2); }
    return std::stoi(argv[++i]);
}
static std::uint64_t require_u64(int& i, int argc, char** argv) {
    if (i + 1 >= argc) { std::cerr << "Missing value after " << argv[i] << "\n"; std::exit(2); }
    return (std::uint64_t)std::stoull(argv[++i]);
}

int main(int argc, char** argv) {
    int k = -1, deg = -1;
    bool printMatching = false;
    std::uint64_t seed = 0;
    std::string algo = "ek";

    for (int i = 1; i < argc; i++) {
        std::string a = argv[i];
        if (a == "--size") k = require_int(i, argc, argv);
        else if (a == "--degree") deg = require_int(i, argc, argv);
        else if (a == "--seed") seed = require_u64(i, argc, argv);
        else if (a == "--printMatching") printMatching = true;
        else if (a == "--algo") { if (i+1>=argc) std::exit(2); algo = argv[++i]; }
        else { std::cerr << "Unknown arg: " << a << "\n"; return 2; }
    }
    if (k < 1) { std::cerr << "--size k required\n"; return 2; }
    if (deg < 0) { std::cerr << "--degree i required\n"; return 2; }

    aod::Timer timer;

    auto inst = aod::generate_bipartite_matching(k, deg, seed);

    aod::FlowStats st;
    long long maxflow = 0;

    if (algo == "dinic") {
        aod::Dinic mf;
        maxflow = mf.run(inst.net, inst.s, inst.t, st);
    } else {
        aod::EdmondsKarp mf;
        maxflow = mf.run(inst.net, inst.s, inst.t, st);
    }

    if (printMatching) {
        const int m = 1 << k;
        const int V1_start = 1;
        const int V2_start = 1 + m;

        for (const auto& ref : inst.forward_edges) {
            int nu = ref.first;
            int idx = ref.second;
            const auto& e = inst.net.adj()[nu][idx];

            long long f = e.orig - e.cap; // 0 albo 1
            if (f == 1) {
                int u = nu - V1_start;      // etykieta w V1: 0..m-1
                int v = e.to - V2_start;    // etykieta w V2: 0..m-1
                std::cout << u << " " << v << "\n";
            }
        }
    }


    std::cout << maxflow << "\n";
    (void)printMatching;

    std::cerr << timer.ms() << "\n";
    return 0;
}

