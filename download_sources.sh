#!/bin/bash

OPENMVG_VERSION="2.0"

if ! [ -d "third_party/openMVG-${OPENMVG_VERSION}" ]; then
  echo "Downloading openMVG-${OPENMVG_VERSION} ..."

  wget "https://github.com/openMVG/openMVG/archive/refs/tags/v${OPENMVG_VERSION}.zip" \
    -O "third_party/openMVG-${OPENMVG_VERSION}.zip"

  unzip -d third_party/ "third_party/openMVG-${OPENMVG_VERSION}.zip"
  rm "third_party/openMVG-${OPENMVG_VERSION}.zip"

  git clone https://github.com/openMVG-thirdparty/cereal.git \
    "third_party/openMVG-${OPENMVG_VERSION}/src/dependencies/cereal"
fi

OPENMVS_VERSION="2.0"

if ! [ -d "third_party/openMVS-${OPENMVS_VERSION}" ]; then
  echo "Downloading openMVS-${OPENMVS_VERSION} ..."

  wget "https://github.com/cdcseacave/openMVS/archive/refs/tags/v${OPENMVS_VERSION}.zip" \
    -O "third_party/openMVS-${OPENMVS_VERSION}.zip"

  unzip -d third_party/ "third_party/openMVS-${OPENMVS_VERSION}.zip"
  rm "third_party/openMVS-${OPENMVS_VERSION}.zip"
fi

if ! [ -d "third_party/vcglib" ]; then
  git clone https://github.com/cdcseacave/VCG.git third_party/vcglib
fi

if ! [ -d "third_party/boost_1_76_0" ]; then
  echo "Downloading boost-1.76 ..."

  wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.zip \
    -O "third_party/boost_1_76_0.zip"

  unzip -d third_party/ third_party/boost_1_76_0.zip
  rm third_party/boost_1_76_0.zip
fi
