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

    BipatiteResoult R = graph.isBipatite();
    if(R.isBipartite){
        if(graph.N()>200){
            cout<<"graf jest dwudzielny";
        }
        else {
            //wypisac podzial na wierzcholki z V0, V1
            vector<int> black;
            cout<<"wierzcholki biale: "<<endl;
            for(int i =0; i<R.color.size(); ++i){
                if(R.color[i] ==1)
                    cout<<i+1<<" ";
                else
                    black.push_back(i);
            }
            cout<<endl<<"wierzcholki czarne: "<<endl;
            for(int i =0; i< black.size(); ++i)
                cout<<black[i]+1<<" ";
        }
    }
    else
        cout<<"graf nie jest dwudzielny";
    cout<<endl;
    return 0;
}

    

