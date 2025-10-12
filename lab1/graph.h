#include <bits/stdc++.h>
using namespace std;

struct Travelsal {
    vector<int> order; //kolejnosc przejscia przez wierzcholki
    vector<int> parent; //kto jest ojcem wierzcholka: u -> parent[u]
    vector<int> dist; //BFS
    vector<int> disc; //DFS pre
    vector<int> fin; //DFS post
};

class Graph {
    private:
        int n; //ilosc wierzcholkow
        int m; //ilosc krawedzi
        bool directed = false; // czy graf skierowany
        vector<pair<int,int>> edges;
        vector<vector<int>> adj; //lista sasiadow

        //funkcje pomocnicze do wczytywania danych
        static inline string trim(const string& s){
            size_t a = s.find_first_not_of(" \t\r\n");
            if(a==string::npos) return "";
            size_t b = s.find_last_not_of(" \t\r\n");
            return s.substr(a, b-a+1);
        }

        static bool nextDataLine(istream& in, string& line){
            while (getline(in, line)) {
                string t = trim(line);
                if (t.empty()) continue;
                line.swap(t);
                return true;
            }
            return false;
        }
    public:
        Graph(ifstream& in);
        ~Graph();
        Travelsal dfs();
        Travelsal bfs();
        void printAdj();
};

