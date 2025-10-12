#include "graph.h"
using namespace std;


int main(int argc, char* argv[]){
    //wczytaj dane podane w wywolaniu
    if(argc !=2){
        cerr<< "uzycie: "<<argv[0]<<" <sciezka do pliku z danymi>"<<endl;
        return 1;
    }
    const string path = argv[1];
    ifstream file(path);
    if(!file){
        cerr<<"nie moge otworzyc pliku "<<path<<endl;
        return 1;
    }
    //skonstroluj graf na podstawie danych z pliku
    Graph graph(file);

    TopologicalResults R = graph.topologicalSort();
    if(graph.N()>200){
        if(R.isDAG)
            cout<<"graf jest DAG";
        else
            cout<<"w grafie jest cykl";
    }
    else {
        if(R.isDAG){
            cout<<"Topologiczne posortowanie grafu:"<<endl;
            for (int i = 0; i<R.order.size(); ++i){
                cout<<R.order[i]<<" ";
            }
        }
        else
            cout<<"w grafie jest cykl";
    }

    return 0;
}

    

