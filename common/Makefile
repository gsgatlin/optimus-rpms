.PHONY: clean install all srpm fc24 fc25 fc26 el6 el7
.SUFFIXES: .spec .rpm
all: build *.src.rpm dist/*.fc24.i686.rpm dist/*.fc24.x86_64.rpm \
dist/*.fc25.i686.rpm dist/*.fc25.x86_64.rpm dist/*.fc26.i686.rpm \
dist/*.fc26.x86_64.rpm dist/*.el6.i686.rpm dist/*.el6.x86_64.rpm \
dist/*.el7.centos.x86_64.rpm dist/*.el7.centos.i686.rpm

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

srpm: *.src.rpm

*.src.rpm: *.spec sources/*
	mkdir -p ./buildroot/SOURCES
	cp -r ./sources/* ./buildroot/SOURCES/
	@echo "Building Source RPM for mock..."
	rpmbuild -bs $(wildcard ./*.spec) --define="_topdir %(pwd)/buildroot"
	cp `find ./buildroot/SRPMS/ -name "*.src.rpm" -type f` ./
	-rm -rf ./buildroot
	
newsrpm = $(shell \ls --color=never *.src.rpm)

fc24: dist/*.fc24.i686.rpm dist/*.fc24.x86_64.rpm 

dist/*.fc24.i686.rpm: build *.src.rpm 
	@echo "Building fc24 i686 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-24-i386 --resultdir=./dist --rebuild $(newsrpm)

dist/*.fc24.x86_64.rpm: build *.src.rpm 
	@echo "Building fc24 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-24-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc25: dist/*.fc25.i686.rpm dist/*.fc25.x86_64.rpm 

dist/*.fc25.i686.rpm: build *.src.rpm 
	@echo "Building fc25 i686 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-25-i386 --resultdir=./dist --rebuild $(newsrpm)

dist/*.fc25.x86_64.rpm: build *.src.rpm 
	@echo "Building fc25 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-25-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc26: dist/*.fc26.i686.rpm dist/*.fc26.x86_64.rpm 

dist/*.fc26.i686.rpm: build *.src.rpm 
	@echo "Building fc26 i686 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-rawhide-i386 --resultdir=./dist --rebuild $(newsrpm)

dist/*.fc26.x86_64.rpm: build *.src.rpm 
	@echo "Building fc26 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-rawhide-x86_64 --resultdir=./dist --rebuild $(newsrpm)

el6: dist/*.el6.i686.rpm dist/*.el6.x86_64.rpm 

dist/*.el6.i686.rpm: build *.src.rpm
	@echo "Building el6 i686 Binary RPMs for mock..."
	mock --verbose --yum --scrub=all --root=epel-6-i386 --resultdir=./dist --rebuild $(newsrpm)

dist/*.el6.x86_64.rpm: build *.src.rpm
	@echo "Building el6 x86_64 Binary RPMs for mock..."
	mock --verbose --yum --scrub=all --root=epel-6-x86_64 --resultdir=./dist --rebuild $(newsrpm)

el7: dist/*.el7.centos.x86_64.rpm dist/*.el7.centos.i686.rpm 

dist/*.el7.centos.x86_64.rpm: build *.src.rpm
	@echo "Building el7 x86_64 Binary RPMs for mock..."
	mock --verbose --yum --scrub=all --root=epel-7-x86_64 --resultdir=./dist --rebuild $(newsrpm)

dist/*.el7.centos.i686.rpm:  build *.src.rpm
	@echo "Building el7 i686 Binary RPMs for mock..."
	mock --verbose --yum --scrub=all --root=../common/mock/mock-centos-7-i386.cfg --resultdir=./dist --rebuild $(newsrpm)

