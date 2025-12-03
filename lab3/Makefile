CXX = g++
CXXFLAGS = -g -std=c++17 -Wall -Wextra -pedantic

OBJS_COMMON = graph.o io.o cli.o algo.o

all: dijkstra dial

dial: dial.o $(OBJS_COMMON)
	$(CXX) $(CXXFLAGS) -o $@ $^

dijkstra: dijkstra.o $(OBJS_COMMON)
	$(CXX) $(CXXFLAGS) -o $@ $^

graph.o: graph.cpp graph.h common.h
	$(CXX) $(CXXFLAGS) -c graph.cpp

io.o: io.cpp io.h graph.h common.h
	$(CXX) $(CXXFLAGS) -c io.cpp

cli.o: cli.cpp cli.h
	$(CXX) $(CXXFLAGS) -c cli.cpp

algo.o: algo.cpp algo.h graph.h common.h
	$(CXX) $(CXXFLAGS) -c algo.cpp

dijkstra.o: dijkstra.cpp graph.h io.h cli.h common.h algo.h
	$(CXX) $(CXXFLAGS) -c dijkstra.cpp

clean:
	rm -f *.o dijkstra dial *.res

.PHONY: all clean

