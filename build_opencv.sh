OPENCV_VERSION="3.4.18"

if [ -d "build-opencv" ]; then
  echo "error: build directory already exists (run ./clean_build.sh to clean it)"
  exit 1
fi

mkdir build-opencv && cd build-opencv

# Configure CMake
cmake "../third_party/opencv-${OPENCV_VERSION}" \
  -DOPENCV_EXTRA_MODULES_PATH="../third_party/opencv_contrib-${OPENCV_VERSION}/modules/"

make -j$(nproc)
cd ..
