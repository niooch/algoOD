#include "graph.h"
using namespace std;

static vector<pair<int,int>> treeEdges(const vector<int>& parent){
    vector<pair<int,int>> e;
    e.reserve(parent.size());
    for(int v=0; v< (int)parent.size(); ++v)
        if(parent[v]!=-1)
            e.emplace_back(parent[v], v);
    return e;
}

int main(int argc, char* argv[]){
    //wczytaj dane podane w wywolaniu
    if(argc !=2 && argc !=3){
        cerr<< "uzycie: "<<argv[0]<<" <sciezka do pliku z danymi> [t]"<<endl;
        return 1;
    }
    const string path = argv[1];
    ifstream file(path);
    if(!file){
        cerr<<"nie moge otworzyc pliku "<<path<<endl;
        return 1;
    }
    bool displayTravelsalTree=false;
    if(argc == 3){
        displayTravelsalTree = true;
    }
    //skonstroluj graf na podstawie danych z pliku
    Graph graph(file);
    Travelsal T = graph.dfs();
    auto E = treeEdges(T.parent);
    
    if(displayTravelsalTree){
        //wypisz drzewo przejscia do zbudowania graficznej wersji
        for (int i =0; i <E.size(); ++i){
            cout<<E[i].first+1 << " "<<E[i].second+1 << endl;
        }
    }
    else{
        //wypisz kolejnosc przeszukania
        for(int i = 0; i<T.order.size(); i++){
            cout<<T.order[i]+1<<" ";
        }
    }
    cout<<endl;


    return 0;
}

    

