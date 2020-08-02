#include <iostream>
#include "hellob.h"
#include "helloa.h"

void helloB(){
    helloA();
    #ifdef NDEBUG
    std::cout << "HelloB Release!" <<std::endl;
    #else
    std::cout << "HelloB Debug!" <<std::endl;
    #endif
}
