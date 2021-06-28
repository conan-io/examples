#include <iostream>
#include "hello.h"

void hello(){
    std::cout << hello_str();
}

std::string hello_str(){
    #ifdef NDEBUG
    return "hello/0.1: Hello World Release!\n";
    #else
    return "hello/0.1: Hello World Debug!\n";
    #endif
}