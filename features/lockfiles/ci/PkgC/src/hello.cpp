#include <iostream>
#include "helloc.h"
#include "helloa.h"

void helloC(){
    helloA();
    #ifdef NDEBUG
    std::cout << "HelloC Release!" <<std::endl;
    #else
    std::cout << "HelloC Debug!" <<std::endl;
    #endif
}
