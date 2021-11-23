#include <iostream>
#include "hello.h"

void hello(){
#ifdef _WIN64
	#ifdef _DEBUG
		std::cout << "Hello World Debug 64!" << std::endl;
	#else
		std::cout << "Hello World Release64!" << std::endl;
	#endif
#else
	#ifdef _DEBUG
		std::cout << "Hello World Debug!" << std::endl;
	#else
		std::cout << "Hello World Release!" << std::endl;
	#endif
#endif

}
