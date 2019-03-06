#include "hello.h"
#include "say.h"

void hello(){
    
	#ifdef NDEBUG
		say("Hello World!");
	#else
		say("Bye World!");
	#endif
}