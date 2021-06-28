#include <iostream>
#include "hello.h"

void hello(){
    #ifdef NDEBUG
    std::cout << "hello/0.1: Hello World Release!" <<std::endl;
    #else
    std::cout << "hello/0.1: Hello World Debug!" <<std::endl;
    #endif
}
