Name:       openmvg
Version:    2.0
Release:    1
Summary:    OpenMVG provides an end-to-end 3D reconstruction from images framework compounded of libraries, binaries, and pipelines.
License:    MPL 2.0
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:   libpng, libjpeg-turbo, libXxf86vm, libXi, libXrandr
Requires:   qt5-qtbase, qt5-qtsvg
Requires:   ceres-solver, flann, coin-or-lemon, coin-or-Clp
BuildRequires: cmake, git, gcc-c++
BuildRequires: libpng-devel, libjpeg-turbo-devel, libXxf86vm-devel, libXi-devel, libXrandr-devel
BuildRequires: qt5-qtbase-devel, qt5-qtsvg-devel
BuildRequires: ceres-solver-devel, flann-devel, coin-or-lemon-devel, coin-or-Clp-devel, cereal-devel

%description
OpenMVG (Multiple View Geometry) is a library for computer-vision scientists and targeted for the Multiple View Geometry community.
It is designed to provide an easy access to:
* Accurate Multiple View Geometry problem solvers,
* Tiny libraries to perform tasks from feature detection/matching to Structure from Motion,
* Complete Structure from Motion pipelines.

%package devel
Summary: OpenMVG development files
Requires: %{name} = %{version}

%description devel
Headers and tools needed for developing with OpenMVG engine.

%prep
git clone --recursive --branch v2.0 --single-branch https://github.com/openMVG/openMVG.git
cd openMVG
git submodule update -i

%build
mkdir openMVG_build
cd openMVG_build

# Configure CMake
cmake ../openMVG/src/ \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DFLANN_INCLUDE_DIR_HINTS=/usr/include/flann \
  -DCOINUTILS_INCLUDE_DIR_HINTS=/usr/include/coin \
  -DCLP_INCLUDE_DIR_HINTS=/usr/include/coin \
  -DOSI_INCLUDE_DIR_HINTS=/usr/include/coin \
  -DLEMON_INCLUDE_DIR_HINTS=/usr/include/lemon

make %{?_smp_mflags}

%install
cd openMVG_build
make DESTDIR=$RPM_BUILD_ROOT install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf openMVG
rm -rf openMVG_build

%files
%defattr(-,root,root,-)
%{_prefix}/bin/*
%{_prefix}/lib/*.a
%{_datadir}/openMVG/sensor_width_camera_database.txt
%{_datadir}/openMVG/webgl/common/*

#%doc COPYING COPYING.LESSER

%files devel
%defattr(-,root,root,-)
%{_includedir}/openMVG/*
%{_includedir}/openMVG_dependencies/
%{_datadir}/openMVG/cmake/*
%{_prefix}/lib/*.cmake

#%doc COPYING COPYING.LESSER

%changelog
# TODO: changelog
