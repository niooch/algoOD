#pragma once
#include <random>
#include <cstdint>
#include <chrono>

namespace aod {

    class RNG {
        public:
            using engine_t = std::mt19937_64;

            explicit RNG(std::uint64_t seed = 0) {
                if (seed == 0) {
                    seed = auto_seed();
                }
                eng_.seed(seed);
            }

            long long uniform_ll(long long l, long long r) {
                std::uniform_int_distribution<long long> dist(l, r);
                return dist(eng_);
            }

            int uniform_int(int l, int r) {
                std::uniform_int_distribution<int> dist(l, r);
                return dist(eng_);
            }

            double uniform01() {
                std::uniform_real_distribution<double> dist(0.0, 1.0);
                return dist(eng_);
            }

            engine_t& engine() { return eng_; }

        private:
            engine_t eng_;

            static std::uint64_t auto_seed() {
                return (std::uint64_t)
                    std::chrono::high_resolution_clock::now()
                    .time_since_epoch()
                    .count();
            }
    };

} 

