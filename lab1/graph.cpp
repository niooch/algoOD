#include "graph.h"

int Graph::N(){
    return n;
}
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

//Zadanie 2. sortowanie topologiczne grafu
//Cormen 22.4
TopologicalResults Graph::topologicalSort(){
    TopologicalResults R;
    //sprawdzenie czy graf jest skierowany
    if(!directed){
        R.isDAG=false;
        return R;
    }
    vector<int> color(n,0); //jak w cormenie 0-bialy, 1-szary, 2-czarny
    vector<int> parent(n,0);
    vector<int> post;
    post.reserve(n);
    bool cycle;

    function<bool(int)> dfsTS = [&](int u)->bool{
        color[u] = 1;
        for (int v: adj[u]){
            if(color[v] == 0){
                parent[v] = u;
                if(dfsTS(v))
                    return true;
            }
            else if (color[v] == 1){
                cycle = true;
                return true;
            }
        }
        color[u] = 2;
        post.push_back(u);
        return false;
    };

    for(int i = 0; i<n; ++i)
        if(color[i]==0)
            if(dfsTS(i))
                break;

    if(cycle){
        R.isDAG=false;
        return R;
    }
    R.isDAG=true;
    R.order.resize(n);
    for(int i = 0; i <n; ++i)
        R.order[i]=post[n-1-i] +1;
    return R;
}
