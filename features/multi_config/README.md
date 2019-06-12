Example of multi-config package with CMake

- Remove the ``build_type`` from settings.
- Have a CMake script that differentiate debug and release artifacts (``set_target_properties(hello PROPERTIES DEBUG_POSTFIX _d)``).
- Have a ``build()`` that builds both configs.
- Have a ``package_info()`` method that accounts for both configs ``self.cpp_info.debug.libs``, etc.


You can build with:

```bash
$ conan test_package -s build_type=Release
# the above will build both debug/Release
$ conan test_package -s build_type=Debug --build=missing
```
