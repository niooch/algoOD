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
    int k = -1;
    bool printFlow = false;
    std::uint64_t seed = 0;
    std::string algo = "ek";

    for (int i = 1; i < argc; i++) {
        std::string a = argv[i];
        if (a == "--size") k = require_int(i, argc, argv);
        else if (a == "--seed") seed = require_u64(i, argc, argv);
        else if (a == "--printFlow") printFlow = true;
        else if (a == "--algo") { if (i+1>=argc) std::exit(2); algo = argv[++i]; }
        else { std::cerr << "Unknown arg: " << a << "\n"; return 2; }
    }
    if (k < 1) { std::cerr << "--size k required\n"; return 2; }

    aod::Timer timer;

    auto inst = aod::generate_hypercube(k, seed);

    aod::FlowStats st;
    long long maxflow = 0;

    if (algo == "dinic") {
        aod::Dinic mf;
        maxflow = mf.run(inst.net, inst.s, inst.t, st);
    } else {
        aod::EdmondsKarp mf;
        maxflow = mf.run(inst.net, inst.s, inst.t, st);
    }
    if (printFlow) {
        for (const auto& ref : inst.forward_edges) {
            int u = ref.first;
            int idx = ref.second;
            const auto& e = inst.net.adj()[u][idx];

            long long f = e.orig - e.cap;   // przepływ na krawędzi forward

            std::cout << u << " " << e.to << " " << f << "\n";
        }
    }


    std::cout << maxflow << "\n";

    // printFlow: zrobimy później na podstawie inst.forward_edges + orig-cap.
    (void)printFlow;

    std::cerr << timer.ms() << "\n";
    std::cerr << st.augmentations << "\n";
    return 0;
}

