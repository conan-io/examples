#pragma once

#include <opencv2/opencv.hpp>
#include "Poco/URIStreamOpener.h"
#include "Poco/StreamCopier.h"
#include "Poco/Path.h"
#include "Poco/URI.h"
#include "Poco/Exception.h"
#include "Poco/SharedPtr.h"
#include "Poco/Net/HTTPStreamFactory.h"
#include "Poco/Net/HTTPSStreamFactory.h"
#include "Poco/Net/FTPStreamFactory.h"
#include "Poco/Net/SSLManager.h"
#include "Poco/Net/AcceptCertificateHandler.h"
#include "Poco/Net/PrivateKeyPassphraseHandler.h"
#include <memory>
#include <iostream>
#include <fstream>

using Poco::Exception;
using Poco::Path;
using Poco::SharedPtr;
using Poco::StreamCopier;
using Poco::URI;
using Poco::URIStreamOpener;
using Poco::Net::AcceptCertificateHandler;
using Poco::Net::Context;
using Poco::Net::FTPStreamFactory;
using Poco::Net::HTTPSStreamFactory;
using Poco::Net::HTTPStreamFactory;
using Poco::Net::InvalidCertificateHandler;
using Poco::Net::SSLManager;

class Downloader
{
public:
	Downloader();
	~Downloader(void);
	std::string DownloadFile(const std::string &url);
};
