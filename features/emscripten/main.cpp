#include <iostream>
#include <zlib.h>

int main()
{
    std::cout << "Using zlib version: " << zlibVersion() << std::endl;
}
