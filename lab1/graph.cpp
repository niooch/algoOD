#include "graph.h"
//funkcje pomocnicze do wczytywania danych

Graph::Graph(ifstream& in){
    string line;
    //wczytaj pokoleji dane

    //czy skierowany
    nextDataLine(in, line);
    char c = toupper(line[0]);
    directed = c =='D';

    //ilosc wierzcholkow
    nextDataLine(in, line);
    n = stoi(line);

    //ilosc krawedzi
    nextDataLine(in, line);
    m = stoi(line);

    //krawedzie
    edges.reserve(m);
    while(nextDataLine(in, line)){
        int u, v; 
        istringstream iss(line);
        iss>>u>>v;
        //zmiana z {1, ..., n} na {0, ..., n-1}
        u--;
        v--;
        edges.emplace_back(u, v);
    }

    //zbuduj liste sasiedztwa
    adj.assign(n, {});
    for (auto [u, v] : edges){
        adj[u].push_back(v);
        if(!directed)
            adj[v].push_back(u);
    }
}

Graph::~Graph()=default;

void Graph::printAdj(){
    for(int i =0; i < adj.size(); ++i){
        cout<<i+1<<": ";
        for (int j = 0; j<adj[i].size(); ++j)
            cout<<adj[i][j]+1<<" ";
        cout<<endl;
    }
}


//zadanie 1 przeszukiwania grafu
//Cormen 22.2
Travelsal Graph::bfs(){
    //init odpowiedzi
    Travelsal T;
    T.parent.assign(n, -1); 
    T.dist.assign(n, -1); 
    T.order.reserve(n);
    
    vector<char> vis(n,0);
    queue<int> q;

    //wiercholek startowy
    vis[0]=1;
    T.dist[0]=0;
    q.push(0);

    while(!q.empty()){
        int u=q.front();
        q.pop();
        T.order.push_back(u);
        for(int v: adj[u]){
            if(!vis[v]){
                vis[v]=1;
                T.parent[v]=u;
                T.dist[v]=T.dist[u]+1;
                q.push(v);
            }
        }
    }

    return T;
}
//Cormen 22.3
Travelsal Graph::dfs(){
    //init odpowiedzi
    Travelsal T;
    T.parent.assign(n, -1); 
    T.disc.assign(n, 0); 
    T.fin.assign(n, 0);
    T.order.reserve(n);
    
    vector<char> vis(n, 0);
    int timer = 0;

    function<void(int,int)> dfsVisit = [&](int u, int p){
        vis[u]=1; 
        T.parent[u]=p;
        T.disc[u]=++timer;
        T.order.push_back(u);
        for(int v: adj[u])
            if(!vis[v])
                dfsVisit(v, u);
        T.fin[u]=++timer;
    };

    dfsVisit(0, -1);
    return T;
}

