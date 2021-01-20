cd recipes
conan create conanfile_go-inject.py
conan create conanfile_go-martini.py
cd ..

conan install conanfile.txt

SET GOPATH=%GOPATH%;%CD%/deps
cd src/server
go build main.go
