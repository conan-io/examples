import requests
import json
import sys
import os

URL = 'https://pypi.python.org/pypi/{package}/json'


def get_conan_version():
    url = URL.format(package='conan')
    response = requests.get(url).text
    version = json.loads(response)['info']['version']
    sys.stdout.write("Last Conan version found: {}\n".format(version))
    return version


def update_tox(last_version):
    conan_prev = 'conan>={major}.{minor_prev},<{major}.{minor}'

    major, minor, _ = last_version.split('.')
    minor_prev = str(int(minor)-1)
    minor_prev_prev = str(int(minor)-2)

    conan_prev = conan_prev.format(major=major, minor=minor, minor_prev=minor_prev, minor_prev_prev=minor_prev_prev)
    sys.stdout.write(" - prev is {major}.{minor_prev}\n".format(major=major, minor_prev=minor_prev, minor_prev_prev=minor_prev_prev))

    # Replace in 'tox.ini' file
    tox_file = os.path.join(os.path.dirname(__file__), '..', 'tox.ini')
    with open(tox_file, 'r') as f:
        content = f.read()

    assert 'conanprev: conan-unknown' in content, "Unexpected tox.ini content"

    content = content.replace('conanprev: conan-unknown', 'conanprev: {}'.format(conan_prev))

    content = content.replace('conancurrent: conan', more_versions)

    with open(tox_file, 'w') as f:
        f.write(content)
    


if __name__ == '__main__':
    v = get_conan_version()
    update_tox(v)
