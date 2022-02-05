#!/bin/bash

OPENMVG_VERSION="2.0"

if [[ -d "build-openmvg" ]]
then
  echo "error: build directory already exists (run ./clean_deps.sh to clean it)"
  exit 1
fi

mkdir build-openmvg && cd build-openmvg

# Configure CMake
cmake "../third_party/openMVG-${OPENMVG_VERSION}/src/" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=/opt/3dr \
  -DFLANN_INCLUDE_DIR_HINTS=/usr/include/flann \
  -DCOINUTILS_INCLUDE_DIR_HINTS=/usr/include/coin \
  -DCLP_INCLUDE_DIR_HINTS=/usr/include/coin \
  -DOSI_INCLUDE_DIR_HINTS=/usr/include/coin \
  -DLEMON_INCLUDE_DIR_HINTS=/usr/include/lemon \

make -j$(nproc)
sudo make install && cd ..
