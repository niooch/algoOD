#include "aod/export/glpk_mathprog.hpp"
#include "aod/graph/flowNetwork.hpp" 

#include <fstream>
#include <stdexcept>

namespace aod {

    void export_maxflow_mathprog(const FlowNetwork& net, int s, int t, const std::string& path) {
        std::ofstream out(path);
        if (!out) throw std::runtime_error("Cannot open file for writing: " + path);

        const int n = net.n();
        const auto& g = net.adj();

        // ===== Model section =====
        out << "set V;\n";
        out << "set A within {V,V};\n";
        out << "param cap{A} >= 0;\n";
        out << "param S integer;\n";
        out << "param T integer;\n\n";

        out << "var x{(i,j) in A} >= 0;\n\n";
        out << "s.t. CapConstr{(i,j) in A}: x[i,j] <= cap[i,j];\n\n";

        out << "s.t. FlowCons{v in V: v <> S and v <> T}:\n";
        out << "  sum{(v,j) in A} x[v,j] - sum{(i,v) in A} x[i,v] = 0;\n\n";

        out << "maximize Obj:\n";
        out << "  sum{(S,j) in A} x[S,j] - sum{(i,S) in A} x[i,S];\n\n";

        out << "solve;\n";
        out << "printf \"maxflow %g\\n\", Obj;\n";
        // UWAGA: NIE DAJEMY tutaj end;

        // ===== Data section =====
        out << "\n";
        out << "data;\n\n";

        out << "set V := ";
        for (int v = 0; v < n; ++v) out << v << " ";
        out << ";\n\n";

        out << "param S := " << s << ";\n";
        out << "param T := " << t << ";\n\n";

        out << "set A :=\n";
        for (int u = 0; u < n; ++u) {
            for (const auto& e : g[u]) {
                if (e.orig > 0) out << "  (" << u << "," << e.to << ")\n";
            }
        }
        out << ";\n\n";

        // Bezpieczny format: u v cap
        out << "param cap :=\n";
        for (int u = 0; u < n; ++u) {
            for (const auto& e : g[u]) {
                if (e.orig > 0) out << "  " << u << " " << e.to << " " << e.orig << "\n";
            }
        }
        out << ";\n\n";

        out << "end;\n"; // JEDYNE end; w całym pliku
    }

} // namespace aod
