# Makefile for Fedora COPR SRPM generation
# This file is used by COPR's SCM build method to generate the SRPM

.PHONY: srpm

srpm:
	# Install required tools
	dnf -y install rpmdevtools rpm-build wget
	
	# Setup rpm build directories
	rpmdev-setuptree
	
	# Copy the spec file to SPECS
	cp $(spec) ~/rpmbuild/SPECS/
	
	# Download the source tarball
	cd ~/rpmbuild/SOURCES && \
	spectool -g -R ~/rpmbuild/SPECS/ModemManager.spec
	
	# Build the SRPM
	rpmbuild -bs ~/rpmbuild/SPECS/ModemManager.spec \
		--define "_srcrpmdir $(outdir)"
	
	@echo "SRPM created in $(outdir)"
