# optimus-rpms

This is an attempt to place the various bumblebee rpms into a version control
repository.

I use "rpmbuild" to build the various source rpms and use "mock" to build 
binary and source rpms for various fedora and RHEL based distros. 

# Instructions

To get started:

dnf install mock

or on RHEL:

yum install mock

Next,

make sure you run

usermod -a -G mock YOURACCOUNTNAME

before you start.

cd into the directory name of the rpm package name you wish to build for.

type 

make

to build for all distros (EL6 EL7 and fedora)

type

make %dist

to build for a specific distro. Like:

make el7

for centos 7 for example.

