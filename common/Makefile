.PHONY: clean install
.SUFFIXES: .spec .rpm
all: build *.src.rpm dist/*.fc24.i686.rpm dist/*.fc24.x86_64.rpm \
dist/*.fc25.i686.rpm dist/*.fc25.x86_64.rpm dist/*.fc26.i686.rpm \
dist/*.fc26.x86_64.rpm dist/*.el6.i686.rpm dist/*.el6.x86_64.rpm \
dist/*.el7.centos.x86_64.rpm
	touch all

install:
	@echo "Error: Cannot stage these rpms in this Makefile"

build: 
	@echo "Creating empty distributable and buildroot directory."
	mkdir -p ./dist
	touch build

clean:
	@echo "Cleaning distributable and buildroot directory."
	-rm -rf ./dist/
	-rm -rf ./buildroot
	-rm -rf $(wildcard ./*.src.rpm)
	-rm -rf ./build
	-rm -rf ./all

*.src.rpm: *.spec sources/*
	mkdir -p ./buildroot/SOURCES
	cp -r ./sources/* ./buildroot/SOURCES/
	@echo "Building Source RPM for mock..."
	rpmbuild -bs $(wildcard ./*.spec) --define="_topdir %(pwd)/buildroot"
	cp `find ./buildroot/SRPMS/ -name "*.src.rpm" -type f` ./
	-rm -rf ./buildroot
	
srpm = $(shell \ls --color=never *.src.rpm)

dist/*.fc24.i686.rpm: build *.src.rpm
	@echo "Building fc24 i686 Binary RPMs for mock..."
	mock --dnf --scrub=all -v -r fedora-24-i386 --rebuild $(srpm) --resultdir=./dist

dist/*.fc24.x86_64.rpm: build *.src.rpm
	@echo "Building fc24 x86_64 Binary RPMs for mock..."
	mock --dnf --scrub=all -v -r fedora-24-x86_64 --rebuild $(srpm) --resultdir=./dist

dist/*.fc25.i686.rpm: build *.src.rpm
	@echo "Building fc25 i686 Binary RPMs for mock..."
	mock --dnf --scrub=all -v -r fedora-25-i386 --rebuild $(srpm) --resultdir=./dist

dist/*.fc25.x86_64.rpm: build *.src.rpm
	@echo "Building fc25 x86_64 Binary RPMs for mock..."
	mock --dnf --scrub=all -v -r fedora-25-x86_64 --rebuild $(srpm) --resultdir=./dist

dist/*.fc26.i686.rpm: build *.src.rpm
	@echo "Building fc26 i686 Binary RPMs for mock..."
	mock --dnf --scrub=all -v -r fedora-rawhide-i386 --rebuild $(srpm) --resultdir=./dist

dist/*.fc26.x86_64.rpm: build *.src.rpm
	@echo "Building fc26 x86_64 Binary RPMs for mock..."
	mock --dnf --scrub=all -v -r fedora-rawhide-x86_64 --rebuild $(srpm) --resultdir=./dist

dist/*.el6.i686.rpm: build *.src.rpm
	@echo "Building el6 i686 Binary RPMs for mock..."
	mock --yum --scrub=all -v -r epel-6-i386 --rebuild $(srpm) --resultdir=./dist

dist/*.el6.x86_64.rpm: build *.src.rpm
	@echo "Building el6 x86_64 Binary RPMs for mock..."
	mock --yum --scrub=all -v -r epel-6-x86_64 --rebuild $(srpm) --resultdir=./dist

dist/*.el7.centos.x86_64.rpm: build *.src.rpm
	@echo "Building el7 x86_64 Binary RPMs for mock..."
	mock --yum --scrub=all -v -r epel-7-x86_64 --rebuild $(srpm) --resultdir=./dist

