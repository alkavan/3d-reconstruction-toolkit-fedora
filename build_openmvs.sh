#!/bin/bash

if [ -d "build-openmvs" ]; then
  echo "error: build directory already exists (run ./clean_deps.sh to clean it)"
  exit 1
fi

if ! [ -d "third_party/boost_1_76_0" ]; then
  echo "unable to find internal boost at 'third_party/boost_1_76_0' (run ./download_sources.sh to download it)"
  exit 1
fi

cd third_party/boost_1_76_0 && ./bootstrap.sh && ./b2 --link=static && cd ../..

OPENMVS_VERSION="2.0"
mkdir build-openmvs && cd build-openmvs

# Configure CMake
cmake "../third_party/openMVS-${OPENMVS_VERSION}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_INSTALL_PREFIX=/opt/3dr \
  -DBOOST_ROOT="../third_party/boost_1_76_0/stage" \
  -DVCG_ROOT="../third_party/vcglib" \
  -DBoost_USE_STATIC_LIBS=ON

make -j$(nproc)
sudo make install && cd ..
