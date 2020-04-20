#include <iostream>
#include "chat.h"

void app(){
    #ifdef NDEBUG
    std::cout << "App Release!" <<std::endl;
    #else
    std::cout << "App Debug!" <<std::endl;
    #endif
    chat();
}
