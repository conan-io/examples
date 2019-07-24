#pragma once

#include <string>

class MyLib
{
public:
	MyLib() = default;
	~MyLib () = default;
	void PrintMessage(const std::string& message);
};

