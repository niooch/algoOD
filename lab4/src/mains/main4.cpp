#include "aod/graph/generators.hpp"
#include "aod/flow/edmondsKarp.hpp"
#include "aod/flow/dinic.hpp"
#include "aod/flow/maxflowBase.hpp"
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>

static int require_int(int& i, int argc, char** argv) {
    if (i + 1 >= argc) { std::cerr << "Missing value after " << argv[i] << "\n"; std::exit(2); }
    return std::stoi(argv[++i]);
}
static std::uint64_t require_u64(int& i, int argc, char** argv) {
    if (i + 1 >= argc) { std::cerr << "Missing value after " << argv[i] << "\n"; std::exit(2); }
    return (std::uint64_t)std::stoull(argv[++i]);
}
static std::string require_str(int& i, int argc, char** argv) {
    if (i + 1 >= argc) { std::cerr << "Missing value after " << argv[i] << "\n"; std::exit(2); }
    return std::string(argv[++i]);
}

static long long now_us() {
    using clk = std::chrono::steady_clock;
    return std::chrono::duration_cast<std::chrono::microseconds>(clk::now().time_since_epoch()).count();
}

int main(int argc, char** argv) {
    // Domyślnie: benchmark task1 dla k=1..16, reps=1
    int task = 1;

    int kmin = 1, kmax = 16;
    int reps = 1;

    // Dla task2:
    // - jeśli imin/imax nie podane, to iterujemy i=1..k (dla każdego k)
    bool have_i_range = false;
    int imin = 1, imax = 1;

    std::uint64_t seed0 = 0; // 0 => auto w generatorze RNG (u Ciebie)

    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "--task") task = require_int(i, argc, argv);
        else if (a == "--kmin") kmin = require_int(i, argc, argv);
        else if (a == "--kmax") kmax = require_int(i, argc, argv);
        else if (a == "--reps") reps = require_int(i, argc, argv);
        else if (a == "--imin") { imin = require_int(i, argc, argv); have_i_range = true; }
        else if (a == "--imax") { imax = require_int(i, argc, argv); have_i_range = true; }
        else if (a == "--seed") seed0 = require_u64(i, argc, argv);
        else {
            std::cerr << "Unknown arg: " << a << "\n";
            return 2;
        }
    }

    if (task != 1 && task != 2) {
        std::cerr << "--task must be 1 or 2\n";
        return 2;
    }
    if (kmin > kmax || kmin < 1) {
        std::cerr << "Invalid k range\n";
        return 2;
    }
    if (reps < 1) {
        std::cerr << "reps must be >= 1\n";
        return 2;
    }

    // CSV header
    if (task == 1) {
        std::cout
            << "task,k,rep,seed,flow,ek_us,ek_aug,dinic_us,dinic_bfs,dinic_dfs,dinic_aug\n";
    } else {
        std::cout
            << "task,k,i,rep,seed,matching,ek_us,dinic_us,dinic_bfs,dinic_dfs\n";
    }

    aod::EdmondsKarp ek;
    aod::Dinic dinic;

    for (int k = kmin; k <= kmax; ++k) {
        if (task == 1) {
            for (int rep = 0; rep < reps; ++rep) {
                // Seed per run: seed0==0 => generator sam zrobi auto_seed, ale wtedy trudniej powtórzyć.
                // Jeśli seed0 != 0 to rozjeżdżamy seed deterministycznie po rep/k.
                std::uint64_t seed = seed0 ? (seed0 + (std::uint64_t)k * 1000003ULL + (std::uint64_t)rep) : 0;

                auto inst = aod::generate_hypercube(k, seed);

                // EK
                aod::FlowStats st_ek;
                auto net_ek = inst.net; // kopia bazowej sieci
                long long t1 = now_us();
                long long f1 = ek.run(net_ek, inst.s, inst.t, st_ek);
                long long t2 = now_us();

                // Dinic
                aod::FlowStats st_d;
                auto net_d = inst.net; // kopia bazowej sieci
                long long t3 = now_us();
                long long f2 = dinic.run(net_d, inst.s, inst.t, st_d);
                long long t4 = now_us();

                if (f1 != f2) {
                    std::cerr << "Mismatch! k=" << k << " rep=" << rep << " ek=" << f1 << " dinic=" << f2 << "\n";
                    return 1;
                }

                std::cout
                    << "1" << "," << k << "," << rep << "," << seed << ","
                    << f1 << ","
                    << (t2 - t1) << "," << st_ek.augmentations << ","
                    << (t4 - t3) << "," << st_d.bfs_runs << "," << st_d.dfs_calls << "," << st_d.augmentations
                    << "\n";
            }
        } else {
            // task2: dla każdego k iterujemy po i (stopień)
            int local_imin = have_i_range ? imin : 1;
            int local_imax = have_i_range ? imax : k; // wg listy zwykle i <= k

            for (int deg = local_imin; deg <= local_imax; ++deg) {
                for (int rep = 0; rep < reps; ++rep) {
                    std::uint64_t seed = seed0 ? (seed0 + (std::uint64_t)k * 1000003ULL + (std::uint64_t)deg * 10007ULL + (std::uint64_t)rep) : 0;

                    auto inst = aod::generate_bipartite_matching(k, deg, seed);

                    // EK
                    aod::FlowStats st_ek;
                    auto net_ek = inst.net;
                    long long t1 = now_us();
                    long long m1 = ek.run(net_ek, inst.s, inst.t, st_ek);
                    long long t2 = now_us();

                    // Dinic
                    aod::FlowStats st_d;
                    auto net_d = inst.net;
                    long long t3 = now_us();
                    long long m2 = dinic.run(net_d, inst.s, inst.t, st_d);
                    long long t4 = now_us();

                    if (m1 != m2) {
                        std::cerr << "Mismatch! k=" << k << " i=" << deg << " rep=" << rep
                            << " ek=" << m1 << " dinic=" << m2 << "\n";
                        return 1;
                    }

                    std::cout
                        << "2" << "," << k << "," << deg << "," << rep << "," << seed << ","
                        << m1 << ","
                        << (t2 - t1) << ","
                        << (t4 - t3) << "," << st_d.bfs_runs << "," << st_d.dfs_calls
                        << "\n";
                }
            }
        }
    }

    return 0;
}

