#!/usr/bin/env bash

set -ex

ROOT=${PWD}
PREFIX=${PWD}/install

mkdir -p build
pushd build

conan install .. -s build_type=Release
cmake .. \
  -DCMAKE_PREFIX_PATH=${PWD} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=${PREFIX}
cmake --build . --target install

TMPDIR=`dirname $(mktemp -u -t tmp.XXXXXXXXXX)`
curl "https://github.com/megastep/makeself/releases/download/release-2.4.0/makeself-2.4.0.run" --output $TMPDIR/makeself.run -L
chmod +x $TMPDIR/makeself.run
$TMPDIR/makeself.run --target $TMPDIR/makeself

python ${ROOT}/deploy.py $PREFIX

$TMPDIR/makeself/makeself.sh $PREFIX ${ROOT}/md5.run "conan-generated makeself.sh" "./conan-entrypoint.sh"

popd

