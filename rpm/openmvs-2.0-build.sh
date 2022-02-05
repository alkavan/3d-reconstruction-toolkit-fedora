#!/bin/bash

sudo dnf builddep -y openmvs-2.0.spec
rpmbuild --undefine=_disable_source_fetch --define "debug_package %{nil}" --clean -ba openmvs-2.0.spec
