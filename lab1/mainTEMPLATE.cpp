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
    //wypisz liste sasiedztwa
    graph.printAdj();
    return 0;
}

    

