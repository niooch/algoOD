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

    SCCResults R = graph.stronglyConnectedComponents();
    //wypisz dane o SCC
    cout<<"liczba SCC: "<<R.count<<","<<endl<<"rozmiary: ";
    for(int i= 0; i <R.count; ++i)
        cout<<R.sizes[i]<<" ";
    if(graph.N()<=200){
        cout<<endl<<"wierzcholki w SCCs:"<<endl;
        for(int i = 0; i<R.count; i++){
            for(int j=0; j<R.componets[i].size(); j++)
                cout<<R.componets[i][j]<<" ";
            cout<<endl;
        }
    }

    return 0;
}

    

