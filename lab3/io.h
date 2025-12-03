//wyczytywanie i zapisywanie plików
#pragma once

#include <string>
#include <vector>
#include <ostream>
#include "graph.h"
#include "common.h"

struct SingleSourceSet {
    std::string sources;
};

SingleSourceSet loadSS(const std::string& path);
void saveSS(
        std::ostream& out,
        const std::string& algoName,
        const std::string& graphFile,
        const std::string& ssFile,
        const GraphMeta& meta,
        double time);

struct PairQuery {
    int s;
    int t;
};
struct P2PQuerySet {
    std::vector<PairQuery> queries;
};

P2PQuerySet loadP2P(const std::string& path);
void saveP2P(
        std::ostream& out,
        const std::string& graphFile,
        const std::string& p2pFile,
        const GraphMeta& meta);
void saveP2PResults(
        std::ostream& out,
        int s,
        int t,
        Distance d);
