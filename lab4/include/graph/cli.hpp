#pragma once
#include <string>
#include <optional>
#include <cstdint>

namespace aod {
    //potrzebne argumenty do przyjecia z linii komend
    enum class Task { Task1 = 1, Task2 = 2 };
    enum class Algo { EdmondsKarp, Dinic };

    struct Options {
        Task task = Task::Task1;
        int size_k = -1;
        int degree_i = -1;

        bool printFlow = false;
        bool printMatching = false;

        Algo algo = Algo::EdmondsKarp;

        std::uint64_t seed = 0;
    };

    Options parse_args(int argc, char** argv);

}

