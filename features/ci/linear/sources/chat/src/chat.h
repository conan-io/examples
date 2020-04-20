#pragma once

#ifdef WIN32
  #define CHAT_EXPORT __declspec(dllexport)
#else
  #define CHAT_EXPORT
#endif

CHAT_EXPORT void chat();
