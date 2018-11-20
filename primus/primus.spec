Summary:        Faster OpenGL offloading for Bumblebee
Name:		primus
Version:        1.1.03282015
URL:            https://github.com/amonakov/primus
Release:        6%{?dist}
License:        ISC
Group:          System Environment/Base
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Source0:	%{name}-master.zip
Patch0:         %{name}-0.2-primuslibglfix.patch
Patch1:         amonakov.patch
Patch2:         %{name}-1.1-libglvndfix.patch
BuildRequires:  unzip
BuildRequires:  mesa-libGL-devel >= 8.0.4
BuildRequires:  libX11-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
Requires:	bumblebee
Requires:	bumblebee-nvidia
Requires:       mesa-libGL%{?_isa} >= 8.0.4
Requires:	mesa-dri-drivers%{?_isa} >= 8.0.4
%if 0%{?rhel} == 6
Requires:       libudev%{?_isa}
BuildRequires:  devtoolset-2-runtime
BuildRequires:  devtoolset-2-gcc
BuildRequires:  devtoolset-2-binutils
BuildRequires:  devtoolset-2-gcc-c++
BuildRequires:  devtoolset-2-libstdc++-devel
%else
Requires:       systemd-libs%{?_isa}
%endif
Provides:       bumblebee-bridge

%description
Primus is a shared library that provides OpenGL and GLX APIs and 
implements low-overhead local-only client-side OpenGL offloading via GLX 
forking, similar to VirtualGL. It intercepts GLX calls and redirects GL 
rendering to a secondary X display, presumably driven by a faster GPU. 
On swapping buffers, rendered contents are read back using a PBO and 
copied onto the drawable it was supposed to be rendered on in the first 
place.

%prep

# extract the source and go into the primus directory

%setup -q -n primus-master

%patch0 -p1 -b .primuslibglfix
%patch1 -p1
%patch2 -p1 -b .libglvndfix

%build

%if 0%{?rhel} == 6
. /opt/rh/devtoolset-2/enable
%endif 

LIBDIR=%{_lib} make %{?_smp_mflags} CFLAGS="%{optflags}"

%install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/%{name}

install -m 755 $RPM_BUILD_DIR/%{name}-master/%{_lib}/libGL.so.1 $RPM_BUILD_ROOT/%{_libdir}/primus/libGL.so.1

mkdir -p $RPM_BUILD_ROOT/%{_bindir}

install -m 755 $RPM_BUILD_DIR/%{name}-master/primusrun $RPM_BUILD_ROOT/%{_bindir}/primusrun

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}

install -m 644 $RPM_BUILD_DIR/%{name}-master/README.md $RPM_BUILD_ROOT/%{_docdir}/%{name}/README.md

install -m 644 $RPM_BUILD_DIR/%{name}-master/technotes.md $RPM_BUILD_ROOT/%{_docdir}/%{name}/technotes.md

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1

install -m 644 $RPM_BUILD_DIR/%{name}-master/primusrun.1  $RPM_BUILD_ROOT/%{_mandir}/man1/primusrun.1

%files
%defattr(-,root,root)
%doc %{_mandir}/man1/primusrun.1.gz
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/technotes.md
%dir %{_libdir}/primus
%{_libdir}/primus/libGL.so.1
%{_bindir}/primusrun

%changelog
* Tue Nov 20 2018 Gary Gatling <gsgatlin@ncsu.edu> - 1.1.03282015-6
- fix for build issues on fedora 29+

* Tue Feb 28 2017 Gary Gatling <gsgatlin@ncsu.edu> - 1.1.03282015-5
- Make package use devtoolset-2 in special mock config on el6.

* Wed Feb 8 2017 Gary Gatling <gsgatlin@ncsu.edu> - 1.1.03282015-4
- Add primus-1.1-libglvndfix.patch because of addition of libglvnd
  to fedora 26 and possibly fedora 25.

* Sat May 28 2016 Gary Gatling <gsgatlin@ncsu.edu> - 1.1.03282015-3
- Fix dependency issues on 64 bit systems using 32 bit multilib.
- Compile on RHEL / CentOS 6 via devtoolset-2. (both i686 and x86_64)
- Add Compile for i686 on RHEL / CentOS 7 via CentOS 7 i686 spin.
- Still not sure whats going on with issue 166. The patch is still included...

* Wed Jun 17 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.1.03282015-2
- Test a patch for issue 
- https://github.com/amonakov/primus/issues/166

* Fri Jun 12 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.1.03282015-1
- Update to newest version.

* Mon Aug 18 2014 Gary Gatling <gsgatlin@ncsu.edu> - 1.0.07112014-1
- Update to newest version.
- Fix for arm build.

* Sun Feb 9 2014 Gary Gatling <gsgatlin@ncsu.edu> - 0.9.02092014-1
- Update to newest version. 

* Fri Sep 20 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.8.09192013-1
- Update to newest version. 

* Sat Aug 10 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.7.08102013-1
- Update to newest version. 

* Sat Jul 20 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.6.07202013-1
- Update to newest version. 

* Sun Jun 2 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.5.06022013-1
- Update to newest version. 

* Sun May 19 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.4.05192013-1
- Update to newest version. 

* Sat May 4 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.3.05042013-1
- Update to newest version. 

* Mon Apr 22 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.2.04222013-1
- Update to newest version. 

* Sun Mar 24 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.1.02252013-2
- Change virtual provides bumblebee-backend to bumblebee-bridge.

* Mon Mar 11 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.1.02252013-1
- Update to newest version. 
- Add virtual provides bumblebee-backend for bumblebee package.

* Fri Jan 25 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.0.12112012-8
- add mesa-dri-drivers dependency and remove bumblebee-nvidia dependency.

* Wed Jan 16 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.0.12112012-7
- update for problem with bumblebee-nvidia package.

* Mon Jan 14 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.0.12112012-6
- clean up specfile and remove more stuff from suse version.

* Sat Jan 12 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.0.12112012-5
- add back in _lib macro to install section.

* Sun Jan 6 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.0.12112012-4
- add primuslibglfix patch and add requirements for mesa >= 8.0.4

* Fri Jan 4 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.0.12112012-3
- remove nouveau driver patch and add bumblebee-nvidia dependency

* Thu Jan 3 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.0.12112012-2
- Clean up specfile and add patch for nouveau driver

* Tue Jan 1 2013 Gary Gatling <gsgatlin@ncsu.edu> - 0.0.12112012-1
- Specfile based on opensuse specfile with modification for fedora/RHEL 6

