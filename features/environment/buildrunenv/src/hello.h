#pragma once

#include <string>

#ifdef WIN32
  #define hello_EXPORT __declspec(dllexport)
#else
  #define hello_EXPORT
#endif

hello_EXPORT void hello();
hello_EXPORT std::string hello_str();
