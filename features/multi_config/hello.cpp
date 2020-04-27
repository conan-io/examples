#include <iostream>
#include "hello.h"

void hello(){
    #if !defined(NDEBUG)
        std::cout << "Hello World Debug!" << std::endl;
    #else
        std::cout << "Hello World Release!" << std::endl;
    #endif
}
