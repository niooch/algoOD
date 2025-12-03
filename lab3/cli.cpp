//kod wczytywania argumentów z linii komend
#include "cli.h"
#include <iostream>

ProgramOptions parseArgs(int argc, char* argv[]){
    if (argc < 5) {
        throw std::runtime_error("za malo argumentow");
    }

    ProgramOptions options;
    bool haveD = false;
    bool haveSS = false;
    bool haveP2P = false;

    for(int i = 1; i <argc; ++i){
        std::string arg = argv[i];
        if (arg == "-d") {
            if (i + 1 >= argc) {
                throw std::runtime_error("brak sciezki do pliku grafu po -d");
            }
            options.graphPath = argv[++i];
            haveD = true;
        } else if (arg == "-ss") {
            if (i + 1 >= argc) {
                throw std::runtime_error("brak sciezki do pliku zrodel po -ss");
            }
            options.mode = Mode::SS;
            options.ssPath = argv[++i];
            haveSS = true;
        } else if (arg == "-oss") {
            if (i + 1 >= argc) {
                throw std::runtime_error("brak sciezki do pliku wynikowego po -oss");
            }
            options.ossPath = argv[++i];
        } else if (arg == "-p2p") {
            if (i + 1 >= argc) {
                throw std::runtime_error("brak sciezki do pliku p2p po -p2p");
            }
            options.mode = Mode::P2P;
            options.p2pPath = argv[++i];
            haveP2P = true;
        } else if (arg == "-op2p") {
            if (i + 1 >= argc) {
                throw std::runtime_error("brak sciezki do pliku wynikowego po -op2p");
            }
            options.op2pPath = argv[++i];
        } else {
            throw std::runtime_error("nieznany argument: " + arg);
        }
    }

    if (!haveD) {
        throw std::runtime_error("brak opcji -d, podaj sciezke do pliku grafu");
    }
    if (haveSS == haveP2P) {
        throw std::runtime_error("podaj dokladnie jedna z opcji -ss lub -p2p");
    }
    if(haveSS){
        if(options.ossPath.empty()){
            throw std::runtime_error("brak sciezki do pliku wynikowego dla trybu ss");
        }
    }
    if(haveP2P){
        if(options.op2pPath.empty()){
            throw std::runtime_error("brak sciezki do pliku wynikowego dla trybu p2p");
        }
    }
    return options;
}

