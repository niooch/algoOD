#pragma once
#include <chrono>

namespace aod {
    class Timer {
        public:
            Timer() : start_(std::chrono::steady_clock::now()) {}
            long long ms() const {
                auto now = std::chrono::steady_clock::now();
                return std::chrono::duration_cast<std::chrono::milliseconds>(now - start_).count();
            }
        private:
            std::chrono::steady_clock::time_point start_;
    };
} 

