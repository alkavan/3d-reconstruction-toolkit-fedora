#!/bin/bash

sudo dnf builddep -y openmvg-2.0.spec
rpmbuild --clean -ba openmvg-2.0.spec


