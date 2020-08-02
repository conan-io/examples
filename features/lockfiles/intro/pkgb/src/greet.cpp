#include <iostream>
#include "hellob.h"

int main(){
    helloB();
    #ifdef NDEBUG
    std::cout << "Greetings Release!" <<std::endl;
    #else
    std::cout << "Greetings Debug!" <<std::endl;
    #endif
}
