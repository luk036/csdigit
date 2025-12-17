//! @file lcsre.cpp
//! @brief Implementation of longest repeated substring algorithm

#include "csdigit/csdigit.hpp"
#include <vector>
#include <algorithm>

namespace csdigit {

std::string longest_repeated_substring(const std::string& cs) {
    size_t n = cs.size();
    std::vector<std::vector<int>> lcsre(n + 1, std::vector<int>(n + 1, 0));
    
    std::string res;
    size_t res_length = 0;
    size_t index = 0;
    
    for (size_t i = 1; i <= n; ++i) {
        for (size_t j = i + 1; j <= n; ++j) {
            if (cs[i - 1] == cs[j - 1] && lcsre[i - 1][j - 1] < static_cast<int>(j - i)) {
                lcsre[i][j] = lcsre[i - 1][j - 1] + 1;
                
                if (lcsre[i][j] > static_cast<int>(res_length)) {
                    res_length = lcsre[i][j];
                    index = std::max(i, index);
                }
            } else {
                lcsre[i][j] = 0;
            }
        }
    }
    
    if (res_length > 0) {
        res = cs.substr(index - res_length, res_length);
    }
    
    return res;
}

} // namespace csdigit