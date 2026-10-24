#pragma once
#include <cmath>
#include <cstdint>
inline bool validReading(float t,float h) {
 return std::isfinite(t)&&std::isfinite(h)&&t>=-40&&t<=80&&h>=0&&h<=100;
}
inline bool due(uint32_t now,uint32_t previous,uint32_t interval) {
 return uint32_t(now-previous)>=interval;
}
