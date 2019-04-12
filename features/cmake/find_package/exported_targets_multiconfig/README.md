Using non-intrusive multi-config CMake with exported targets & find_package
===========================================================================

In this example
---------------

We are using CMake to declare, export and install the targets of a `bye` library that depends on a `hello` library.
Then using Conan to manage the packages and using these libraries in a project. 

**NOTE**: *This is not* the recommended way to use Conan based on ``find_package`` (look at the "cons") but indeed a possibility.

Everything is based on the ``find_package`` feature and working with  multi-config packages (Release/Debug) to avoid 
installing the dependencies every time we change from Debug to Release in the Visual Studio IDE.

 - We have a "hello" library consumed by a "bye" library and a "project" that uses the "bye" function.
 - The "hello" library exports its own ``helloTargets.cmake`` files, everything is pure CMake, every time we call 
   CMake with a different build type CMake exports a ``helloTargets-{build_type}.cmake`` script.
 - The conan recipe uses the same binary package for any ``build_type``, by removing the ``build_type`` setting.
 - The conan recipe at the ``build`` method invokes CMake both for Release and Debug, generating for the same package.
 - The same for the "bye" library.
 

Some useful details of this example
------------------------------------

 - The ``CMakeLists.txt`` of the consumer project (at folder project) calls only ``find_package`` to manage
 the dependencies transparently (both with ``bye`` and ``hello``):

```
cmake_minimum_required(VERSION 3.0)
project(PackageTest CXX)

find_package(bye)
add_executable(example example.cpp)
target_link_libraries(example bye::bye)
```
 
 - The ``CMakeLists.txt`` files for ``bye`` and ``hello`` are quite similar, the same code except the library name and
 dependencies are changed in the first part. So you could use a similar ``CMakeLists.txt`` if you want to follow this 
 approach.
 - The ``helloConfig.cmake`` and ``byeConfig.cmake`` are not auto-generated. They have to manually call `find_dependency`
 for all the dependencies and then include the targets. In this case, the ``bye`` library needs to find the ``hello``:
 
 ```
 include(CMakeFindDependencyMacro)
 find_dependency(hello)

 include("${CMAKE_CURRENT_LIST_DIR}/byeTargets.cmake")
 ```

 - The recipes are not even using ``package_info()``  method for the consumers

Pros
----

- If you are going to consume your packages only with CMake, this is a totally non-intrusive and decoupled mechanism.
- You don't need to change anything in the ``CMakeLists.txt`` related to Conan.
- The multi-config mechanism works good, it is very comfortable, only one ``conan install`` for the dependencies.

 
Cons
----
 
 - You cannot consume Conan packages with other mechanism than ``CMake find_package``, no ``package_info`` method has been
 declared. The logic for the consumer lives exclusively in the ``.cmake`` files installed by CMake, so if I want to use
 any package with other build system like ``Autotools`` I won't be able to do it.

 - Any other information about the libraries that a classic ``self.cppinfo`` object might have (like a compilation flag or definition), 
 won't be applied to the targets automatically.
 
 - You need to build packages containing all the build_types in the same Conan binary package. The ``find_package``
 mechanism will find only one ``XXXConfig.cmake`` file, so all the ```XXXTarget-{build_type}``` have to be together.
 
 - The targets are transitive but you need to "model" the dependencies in the ``XXXConfig.cmake`` files, by calling ``find_dependency``, so you are
 duplicating information that Conan already knows (dependency graph).
 

How to try it
-------------

 - Open the "build.bat" or "build.sh" to see the steps of the example. If you run it, it will create the packages for "hello" and "bye" 
 and will build the "project" changing the build_type and verifying that the linked dependencies are correct for the selected build_type.