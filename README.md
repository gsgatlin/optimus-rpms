# optimus-rpms

This is an attempt to place the various bumblebee rpms into a version control
repository.

I use "rpmbuild" to build the various source rpms and use "mock" to build 
binary and source rpms for various fedora and RHEL based distros. 

# Instructions

1. Install mock: `dnf install mock` 

2. Add yourself to the "mock" group: `usermod -a -G mock YOURACCOUNTNAME`

3. cd into the directory of the rpm package you wish to build.

4. Build:
   - For all distros run: `make`
   - For a specific distro run: `make %dist` (e.g `make el7` for CentOS 7)

Some new build options exist which are not part of "all" which are:

make rhelbeta8 

This build process only works on the fedora distribution at this time. 
Obviously the resultant binary rpms should be installed in the proper 
distro such as CentOS 6, EL7, etc.

