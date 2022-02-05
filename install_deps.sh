#!/bin/bash

echo "Installing runtime dependencies for OpenMVG ..."
sudo dnf install libpng libjpeg-turbo libXxf86vm libXi libXrandr \
  qt5-qtbase qt5-qtsvg ceres-solver flann coin-or-lemon coin-or-Clp

echo "Installing runtime dependencies for OpenMVS ..."
sudo dnf install libpng libjpeg-turbo libtiff opencv ceres-solver glfw

echo "Installing common build dependencies ..."
sudo dnf install cmake git gcc-c++ wget unzip \
  libpng-devel libjpeg-turbo-devel ceres-solver-devel

echo "Installing build dependencies for OpenMVG ..."
sudo dnf install  libXxf86vm-devel libXi-devel libXrandr-devel \
  qt5-qtbase-devel qt5-qtsvg-devel  flann-devel coin-or-lemon-devel coin-or-Clp-devel cereal-devel

echo "Installing build dependencies for OpenMVS ..."
sudo dnf install libtiff-devel opencv-devel CGAL-devel CGAL-qt5-devel glfw-devel glew-devel
