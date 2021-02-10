#include "downloader.h"
#include <iterator>

Downloader::Downloader(void)
{
	HTTPStreamFactory::registerFactory();
	FTPStreamFactory::registerFactory();
	HTTPSStreamFactory::registerFactory();
	Poco::Net::initializeSSL();
}

Downloader::~Downloader(void)
{
	Poco::Net::uninitializeSSL();
}

std::string Downloader::DownloadFile(const std::string &url)
{
	Path path(url);
	std::string filename = "";
	try
	{
		SharedPtr<InvalidCertificateHandler> pCertHandler = new AcceptCertificateHandler(false);
		Context::Ptr pContext = new Context(Context::CLIENT_USE, "");
		SSLManager::instance().initializeClient(0, pCertHandler, pContext);
		URI uri(url);
		std::unique_ptr<std::istream> pStr(URIStreamOpener::defaultOpener().open(uri));
		std::ofstream fileStream;
		filename = path.getFileName();
		fileStream.open(filename, std::ios::out | std::ios::trunc | std::ios::binary);
		StreamCopier::copyStream(*pStr.get(), fileStream);
		fileStream.close();
	}
	catch (Exception &exc)
	{
		std::cerr << exc.displayText() << std::endl;
		filename = "";
	}
	return filename;
}
