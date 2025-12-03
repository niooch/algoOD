//parsowanie opcji wiersza poleceń
#pragma once
#include <string>
#include <stdexcept>

enum class Mode {
    SS,
    P2P
};

struct ProgramOptions {
    std::string graphPath;
    Mode mode;
    std::string ssPath;
    std::string ossPath;
    std::string p2pPath;
    std::string op2pPath;
};

ProgramOptions parseArgs(int argc, char* argv[]);
