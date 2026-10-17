#include "../firmware/WeatherStation/logic.h"
#include <cassert>
#include <iostream>
int main(){
 assert(validReading(25,50)); assert(validReading(-40,0));assert(validReading(80,100));
 assert(!validReading(NAN,50)); assert(!validReading(25,NAN));assert(!validReading(INFINITY,50));
 assert(!validReading(-41,50));assert(!validReading(81,50));assert(!validReading(25,-1));assert(!validReading(25,101));
 assert(!due(19999,0,20000));assert(due(20000,0,20000));
 assert(due(0x10u,0xfffffff0u,32));assert(!due(0x10u,0xfffffff0u,33));
 std::cout<<"PASS: 14 assertions (sensor bounds, invalid samples, timing and millis rollover).\n";
}
