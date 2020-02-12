#include "Poco/MD5Engine.h"
#include "Poco/DigestStream.h"

#include <iostream>

int main(int argc, char** argv)
{
    Poco::MD5Engine md5;
    std::string s = "abcdefghijklmnopqrstuvwxyz";
    Poco::DigestOutputStream ds(md5);
    ds << s;
    ds.close();
    std::cout << "MD5 of \"" << s << "\":" << std::endl;
    std::cout << Poco::DigestEngine::digestToHex(md5.digest()) << std::endl;
    return 0;
}
