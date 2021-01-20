# Conan go server example

## How to use

Install **conan** from [Conan.io](https://conan.io)


Build all recipes:

    cd recipes/
	conan create conanfile_go-inject.py
	conan create conanfile_go-inject.py


Install your requires in "deps" folder:

	conan install conanfile.txt


Include "deps" folder in GOPATH and run!


	export GOPATH=${PWD}:${PWD}/deps
	cd src/server
	go run main.go
