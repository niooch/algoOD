//main dla algorytmu Radixheap
#include <iostream>
#include <vector>
#include <fstream>
#include <unordered_map>
#include <chrono>
#include "common.h"
#include "graph.h"
#include "io.h"
#include "cli.h"
#include "algo.h"

int main(int argc, char* argv[]){
    try{
        ProgramOptions options = parseArgs(argc, argv);

        Graph g;
        GraphMeta meta = loadGraph(options.graphPath, g);

        if (options.mode == Mode::SS) {
            SingleSourceSet ss = loadSS(options.ssPath);
            if (ss.sources.empty()) {
                throw std::runtime_error("brak zrodel w pliku zrodla -ss");
            }

            std::vector<Distance> dist;
            double elapsed = 0.0;
            int count = 0;

            for(int s : ss.sources){
                auto start = std::chrono::high_resolution_clock::now();
                radixheap(g, s, dist);
                auto end = std::chrono::high_resolution_clock::now();
                elapsed += std::chrono::duration<double, std::milli>(end - start).count();
                count++;
            }

            double avgTime = elapsed / count;

            std::ofstream out(options.ossPath);
            if (!out.is_open()) {
                throw std::runtime_error("Nie mozna otworzyc pliku wyjsciowego");
            }

            saveSS(out, "radixheap", options.graphPath, options.ssPath, meta, avgTime);
            out.close();
        }
        else if (options.mode == Mode::P2P) {
            P2PQuerySet p2p = loadP2P(options.p2pPath);
            if (p2p.queries.empty()) {
                throw std::runtime_error("brak par w pliku punkt-do-punktu -p2p");
            }

            std::ofstream out(options.op2pPath);
            if (!out.is_open()) {
                throw std::runtime_error("Nie mozna otworzyc pliku wyjsciowego");
            }

            saveP2P(out, options.graphPath, options.p2pPath, meta);
            std::unordered_map<int, std::vector<std::size_t>> bySource;
            bySource.reserve(p2p.queries.size());

            for (std::size_t i = 0; i < p2p.queries.size(); ++i) {
                bySource[p2p.queries[i].s].push_back(i);
            }

            std::vector<Distance> dist;
            std::vector<Distance> results(p2p.queries.size(), INF);

            for (auto& kv : bySource) {
                int s = kv.first;
                const auto& indices = kv.second;

                radixheap(g, s, dist);

                for (std::size_t idx : indices) {
                    int t = p2p.queries[idx].t;
                    if(t>=0 && t < static_cast<int>(dist.size())){
                        results[idx] = dist[t];
                    }
                }
            }

            for (std::size_t i = 0; i < p2p.queries.size(); ++i) {
                saveP2PResults(out, p2p.queries[i].s, p2p.queries[i].t, results[i]);
            }
        }
        else {
            throw std::runtime_error("Nieznany tryb dzialania programu");
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Blad: " << e.what() << std::endl;
        std::cerr << "Przyklad uzycia:\n"
                  << "  radixheap -d plik_z_danymi.gr -ss zrodla.ss -oss wyniki.ss.res\n"
                  << "  radixheap -d plik_z_danymi.gr -p2p pary.p2p -op2p wyniki.p2p.res\n";
        return 1;
    }
    return 0;
}
