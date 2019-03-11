Using unobtrusive multi-config CMake with cmake_find_package_generator_multi
============================================================================

In this example
---------------

We are using Conan to create for us the necessary findXXX scripts both for Release and Debug. 
Everything is based on the ``find_package`` feature and working with  multiconfig packages (Release/Debug) to avoid 
installing the dependencies every time we change from Debug to Release in the Visual Studio IDE.

 - We have a "hello" library consumed by a "bye" library and a project that uses the "bye" function.
 - The "hello" library has a ``package_info()`` method declaring the "hello" library name for the consumers.
 - The conan recipe uses a different binary package for any ``build_type``, one package for Debug and other for Release.
 - The same for the "bye" library.
 - There are two consumer projects, one using targets (CMake 3.x) and other following the global approach (2.8), both
   work with multiconfig.
 
Some useful details of this example
------------------------------------

 - The ``CMakeLists.txt`` files for ``bye`` and ``hello`` are very simple, we are not installing nor exporting anything.
 
  This is the one for ``bye``: 
  ```cmake
  find_package(hello)
  add_library(bye bye.cpp)
  target_link_libraries(bye hello::hello)
  ```

 - The recipes are using ``package_info()``  method for the consumers
 - The recipes are using ``package()`` method to extract the libraries and headers, instead of using cmake install.

Pros
----

- You can consume the conan packages for ``hello`` and ``bye`` from any build system only specifying the generator
  that matches your needs. 
- You don't need to change anything in the ``CMakeLists.txt`` related to Conan.
- The multi-config mechanism works good, it is very comfortable, You call ``conan install`` for debug and other for Release
  and you are done.
- It works for target approach (CMake 3) and global approach (CMake 2.8).
 
Cons
----
 
 - The name of the targets that the ``cmake_find_package_multi`` generates cannot be configured. They are ``package_name::package_name``,
   so maybe it doesn't match the "standard" find script provided by CMake and you might need to change your code or create an alias target.
 - You still have to take care of adjusting the runtime in the CMakeLists.txt to avoid conflicts. The ``cmake`` generator 
   do it automatically, but STILL not the ``cmake_find_package`` nor ``cmake_find_package_multi``. 
 
How to try it
-------------

 - Open the "run.bat" to see the steps of the example. If you run it, it will create the packages for "hello" and "bye" 
 and will build the "project" changing the build_type and verifying that the linked dependencies are correct for the selected build_type.
 