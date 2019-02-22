#include <iostream>
#include <string>
#include "say.h"

void say(std::string msg){
    #ifdef NDEBUG
    std::cout << "Release: " << msg <<std::endl;
    #else
    std::cout << "Debug: " << msg <<std::endl;
    #endif
}