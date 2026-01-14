CXX      := g++
CXXFLAGS := -std=c++17 -O2 -Wall -Wextra -Wshadow -Wconversion -Iinclude
LDFLAGS  :=

BUILD := build

COMMON_SRCS := \
  src/common/timer.cpp \
  src/graph/flowNetwork.cpp \
  src/graph/generators.cpp \
  src/flow/edmondsKarp.cpp \
  src/flow/dinic.cpp

COMMON_OBJS := $(COMMON_SRCS:src/%.cpp=$(BUILD)/%.o)

TASK1_APP := $(BUILD)/task1
TASK2_APP := $(BUILD)/task2
TASK4_APP := $(BUILD)/task4

TASK1_MAIN := src/mains/main1.cpp
TASK2_MAIN := src/mains/main2.cpp
TASK4_MAIN := src/mains/main4.cpp

TASK1_OBJ := $(TASK1_MAIN:src/%.cpp=$(BUILD)/%.o)
TASK2_OBJ := $(TASK2_MAIN:src/%.cpp=$(BUILD)/%.o)
TASK4_OBJ := $(TASK4_MAIN:src/%.cpp=$(BUILD)/%.o)

.PHONY: all clean run1 run2

all: $(TASK1_APP) $(TASK2_APP) $(TASK4_APP)

$(TASK1_APP): $(COMMON_OBJS) $(TASK1_OBJ)
	$(CXX) $^ -o $@ $(LDFLAGS)

$(TASK2_APP): $(COMMON_OBJS) $(TASK2_OBJ)
	$(CXX) $^ -o $@ $(LDFLAGS)

$(TASK4_APP): $(COMMON_OBJS) $(TASK4_OBJ)
	$(CXX) $^ -o $@ $(LDFLAGS)

$(BUILD)/%.o: src/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD)

#test runs
run1: $(TASK1_APP)
	$(TASK1_APP) --size 5 --algo ek

run2: $(TASK2_APP)
	$(TASK2_APP) --size 6 --degree 3 --algo ek

