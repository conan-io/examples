#include "../include/mylib.hpp"

#include <iostream>

MyLib::MyLib()
{
}


MyLib::~MyLib()
{
}

void MyLib::PrintMessage(const std::string & message)
{
	std::cout << message << std::endl;
}

