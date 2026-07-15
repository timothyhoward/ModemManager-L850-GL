# Makefile for Fedora COPR SRPM generation
# This file is used by COPR's SCM build method to generate the SRPM
#
# Usage: COPR calls this with:
#   make -f .copr/Makefile srpm outdir="<outdir>" spec="<spec_path>"
#
# The spec parameter is the path to whichever .spec file you configure
# in the COPR package settings (e.g., ModemManager.spec, dependencies/libqmi.spec)

.PHONY: srpm

# Extract just the filename from the spec path
SPEC_FILE = $(notdir $(spec))

srpm:
	# Install required tools
	dnf -y install rpmdevtools rpm-build wget

	# Setup rpm build directories
	rpmdev-setuptree

	# Ensure directories exist
	mkdir -p ~/rpmbuild/{SOURCES,SPECS,SRPMS}

	# Copy the spec file to SPECS
	cp $(spec) ~/rpmbuild/SPECS/

	# Copy repository-local patches to RPM's configured source directory.
	# COPR overrides this to /builddir/build/SOURCES instead of ~/rpmbuild/SOURCES.
	mkdir -p "$$(rpm --eval '%{_sourcedir}')"
	cp patches/*.patch "$$(rpm --eval '%{_sourcedir}')/"
	
	# Download the source tarball(s) defined in the spec
	cd ~/rpmbuild/SOURCES && \
	spectool -g -R ~/rpmbuild/SPECS/$(SPEC_FILE)
	
	# Build the SRPM
	rpmbuild -bs ~/rpmbuild/SPECS/$(SPEC_FILE) \
		--define "_srcrpmdir $(outdir)"
	
	@echo "SRPM created in $(outdir)"
