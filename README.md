# 3D Reconstruction Toolkit (for Fedora Linux)
The following package contains scripts to build and install
[OpenMVG](https://github.com/openMVG/openMVG/)
and [OpenMVS](https://github.com/cdcseacave/openMVS)
manually into `/opt/3dr/` on Fedora Linux.
Additionally, the package provides RPM spec files and scripts for building RPM packages:
* `rpm/openmvg-2.0.spec`
* `rpm/openmvs-2.0.spec`

Currently, it's recommended to use the build scripts and not the package files
because binaries of both software are not following UNIX conventions and are installed into strange paths.

## Install instruction for `opt/3dr/`
Install system dependencies and download sources
```
./install_deps.sh
./download_sources.sh
```

Build and install OpenMVG
```
./build_openmvg.sh
```

Build and install OpenMVS
```
./build_openmvs.sh
```

You should find installed software in the `/opt/3dr` prefix.

Run `./clean_build.sh` to clean build directories.
