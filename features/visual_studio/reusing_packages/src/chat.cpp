#include "chat.h"
#include "hello.h"

void chat(){
    #ifdef _DEBUG
    hello();
    hello();
    hello();
    #else
    hello();
    hello();
    #endif
}
