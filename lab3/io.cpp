//kod wczytywania i zapisywania plików
#include "io.h"
#include <fstream>
#include <stdexcept>
#include <iostream>

SingleSourceSet loadSS(const std::string& path) {
    std::ifstream in(path);
    if (!in){
        throw std::runtime_error("nie moge otworzyc pliku: " + path);
    }

    SingleSourceSet ss;
    std::string token;

    while (in >> token) {
        if (token == "c"){//komentarz
            std::string comment;
            std::getline(in, comment); //skip
        } else if (token == "p") { //definicja problemu > p aux sp ss K
            std::string aux, sp, type;
            int K;
            in >> aux >> sp >> type >> K;
        } else if (token == "s") { //definicja zródła > s node
            int s;
            in >> s;
            if (!in) {
                throw std::runtime_error("blad w zaczytywaniu zrodla s: " + path);
            }
            ss.sources.push_back(s);
        } else {
            std::getline(in, token); //skip nieznane linie
        }
    }
    return ss;
}

P2PQuerySet loadP2P(const std::string& path) {
    std::ifstream in(path);
    if (!in){
        throw std::runtime_error("nie moge otworzyc pliku: " + path);
    }

    P2PQuerySet p2p;
    std::string token;

    while (in >> token) {
        if (token == "c"){//komentarz
            std::string comment;
            std::getline(in, comment); //skip
        } else if (token == "p") { //definicja problemu > p aux sp p2p K
            std::string aux, sp, type;
            int K;
            in >> aux >> sp >> type >> K;
        } else if (token == "q") { //definicja zapytania > q s t
            PairQuery query;
            in >> query.s >> query.t;
            if (!in) {
                throw std::runtime_error("blad w zaczytywaniu zapytania q: " + path);
            }
            p2p.queries.push_back(query);
        } else {
            std::getline(in, token); //skip nieznane linie
        }
    }
    return p2p;
}

void saveSS(
        std::ostream& out,
        const std::string& algoName,
        const std::string& graphFile,
        const std::string& ssFile,
        const GraphMeta& meta,
        double time) {
    out << "c Plik wynikowy dla problemu najkrotszej sciezki z jednym zrodlem\n";
    out << "c Algorytm: " << algoName << "\n";
    out << "p res sp ss " <<algoName << "\n";
    out << "c\n";
    out << "c Plik testowy grafu: " << graphFile << "\n";
    out << "c Plik testowy zrodel: " << ssFile << "\n";
    out << "f " << graphFile << " " << ssFile << "\n";
    out << "c\n";
    out << "c Siec sklada sie z " << meta.n << " wierzcholkow i " << meta.m << " krawedzi.\n";
    out << "c Koszt krawedzi zawiera sie w przedziale [" << meta.minCost << ", " << meta.maxCost << "].\n";
    out << "g " << meta.n << " " << meta.m << " " << meta.minCost << " " << meta.maxCost << "\n";
    out << "c\n";
    out << "c Sredni czas wyznaczenia najkrotszych sciezek między zrodlem a wszystkimi wierzcholkami: " << time << " ms.\n";
    out << "t " << time << "\n";
}

void saveP2P(
        std::ostream& out,
        const std::string& graphFile,
        const std::string& p2pFile,
        const GraphMeta& meta) {
    out << "c plik wynikowy dla problemu\n";
    out << "c najkrotszej sciezki miedzy para wierzcholkow.\n";
    out << "c\n";
    out << "c wyniki testu dla sieci zadanej w pliku " << graphFile << "\n";
    out << "c i par zrodlo-ujscie podanych w pliku " << p2pFile << ":\n";
    out << "f " << graphFile << " " << p2pFile << "\n";
    out << "c\n";
    out << "c siec sklada sie z " << meta.n << " wierzcholkow, "
        << meta.m << " lukow,\n";
    out << "c koszty naleza do przedzialu ["
        << meta.minCost << "," << meta.maxCost << "]:\n";
    out << "g " << meta.n << " " << meta.m << " "
        << meta.minCost << " " << meta.maxCost << "\n";
    out << "c\n";
    out << "c dlugosci najkrotszych sciezek\n";
}

void saveP2PResults(
        std::ostream& out,
        int s,
        int t,
        Distance d) {
    if (d >= INF / 2) {
        out << "u " << s << " " << t << " INF\n";
    } else {
        out << "d " << s << " " << t << " " << d << "\n";
    }
}
