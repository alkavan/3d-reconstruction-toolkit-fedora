Name: openmvs
Version: 2.0
Release: 1
Summary: Open Multi-View Stereo reconstruction library
License: AGPL 3.0
Source: https://github.com/cdcseacave/openMVS/archive/refs/tags/v2.0.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: libpng, libjpeg-turbo, libtiff, opencv, ceres-solver, glfw
BuildRequires: wget, unzip, cmake, git, gcc-c++
BuildRequires: libpng-devel, libjpeg-turbo-devel, libtiff-devel, opencv-devel, CGAL-devel, CGAL-qt5-devel, ceres-solver-devel, glfw-devel, glew-devel

%description
OpenMVS (Multi-View Stereo) is a library for computer-vision scientists and especially targeted to the Multi-View Stereo reconstruction community.

%package devel
Summary: OpenMVS development files
Requires: %{name} = %{version}

%description devel
Headers and tools for developing OpenMVS applications and libraries.

%prep
%setup -c
git clone https://github.com/cdcseacave/VCG.git vcglib

wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.zip
unzip boost_1_76_0.zip

%build
cd boost_1_76_0 && ./bootstrap.sh && ./b2 --link=static
cd ..

mkdir openMVS_build && cd openMVS_build

# Configure CMake
cmake ../openMVS-%{version} \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DBOOST_ROOT="../boost_1_76_0/stage" \
  -DVCG_ROOT="../vcglib" \
  -DBoost_USE_STATIC_LIBS=ON

make %{?_smp_mflags}

%install
cd openMVS_build
make DESTDIR=$RPM_BUILD_ROOT install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/OpenMVS/*
%{_exec_prefix}/lib/OpenMVS/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/OpenMVS/*
%{_exec_prefix}/lib/cmake/OpenMVS/*.cmake

%changelog
# TODO: changelog
