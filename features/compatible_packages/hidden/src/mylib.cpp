
#include <utility>
#include "../include/mylib.h"

auto compute(int a, float b) -> float {
    auto p = std::make_pair(a, b);
    return std::get<int>(p)/std::get<float>(p);
}
