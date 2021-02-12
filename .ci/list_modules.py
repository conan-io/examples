import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

dists = importlib_metadata.distributions()
installed_packages_list = sorted(
    ["%s==%s" % (dist.metadata["Name"], dist.version) for dist in dists])
print(installed_packages_list)
