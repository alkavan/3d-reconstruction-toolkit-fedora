#!/bin/bash

OPENMVS_VERSION="2.0.1"

if [ -d "build-openmvs" ]; then
  echo "error: build directory already exists (run ./clean_build.sh to clean it)"
  exit 1
fi

if ! [ -d "third_party/boost_1_76_0" ]; then
  echo "unable to find internal boost at 'third_party/boost_1_76_0' (run ./download_sources.sh to download it)"
  exit 1
fi

cd third_party/boost_1_76_0 && ./bootstrap.sh && ./b2 --link=static
cd ../../

mkdir build-openmvs && cd build-openmvs

# Configure CMake
cmake "../third_party/openMVS-${OPENMVS_VERSION}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_INSTALL_PREFIX=/opt/3dr \
  -DBOOST_ROOT="../third_party/boost_1_76_0/stage" \
  -DVCG_ROOT="../third_party/vcglib" \
  -DBoost_USE_STATIC_LIBS=ON

# -DOpenCV_ROOT="../build-opencv" \

make -j$(nproc)
sudo make install && cd ..
