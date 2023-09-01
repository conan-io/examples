cd recipes
conan create conanfile_go-inject.py
conan create conanfile_go-martini.py
cd ..

conan install conanfile.txt

export GOPATH=${GOPATH}:${PWD}/deps
cd src/server
go build main.go
