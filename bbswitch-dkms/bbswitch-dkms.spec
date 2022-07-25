# Module is built by dkms, we don't have any debuginfo at package build time
%global debug_package %{nil}
%define module bbswitch

Summary:        Linux kernel module for Bumblebee
Name:           %{module}-dkms
Version:        0.8.0
URL:            https://github.com/Bumblebee-Project/bbswitch/
Release:        5%{?dist}
License:        GPLv3
Group:          System Environment/Base
Source0:        %{module}-0.8.tar.gz
Source1:        %{module}.conf
Source2:        %{module}.modules
Patch0:         %{module}-412.patch
Patch1:         %{module}-56.patch
Patch2:         %{module}-518.patch
BuildRoot:      %{_tmppath}/%{name}-root
%ifarch i686
%if 0%{?fedora} >=15
Requires:       kernel-PAE-devel
%endif
%endif
Requires:       dkms gcc kernel-devel make
Conflicts:      bbswitch

%description
bbswitch within the bbswitch-dkms package is a Linux kernel module which 
automatically detects the required ACPI calls for two kinds of Optimus 
laptops. It has been verified to work with "real" Optimus and "legacy" 
Optimus laptops.


See: https://github.com/Bumblebee-Project/bbswitch/

For further information.

For now, if you require nvidia module support with bumblebee you must 
install bbswitch-dkms.

%prep

%setup -q -n %{module}-0.8


%if 0%{?fedora:1} || 0%{?rhel} >= 8
%patch0 -p1 -b .4.12fix
%endif
%patch1 -p1 -b .5.6fix
%patch2 -p1 -b .518fix


%build

%install

rm -rf ${RPM_BUILD_ROOT}

install -d -m 755 %{buildroot}%{_prefix}/src
install -d -m 755 %{buildroot}%{_prefix}/src/%{module}-%{version}
install -pm 644 bbswitch.c %{buildroot}%{_prefix}/src/%{module}-%{version}
install -pm 644 Makefile %{buildroot}%{_prefix}/src/%{module}-%{version}
install -pm 644 dkms/dkms.conf %{buildroot}%{_prefix}/src/%{module}-%{version}

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -pm 644 COPYING %{buildroot}%{_docdir}/%{name}/
install -pm 644 NEWS %{buildroot}%{_docdir}/%{name}/
install -pm 644 README.md %{buildroot}%{_docdir}/%{name}/

%if 0%{?fedora:1} || 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT/etc/modules-load.d/
install -pm 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/modules-load.d/
%endif

%if 0%{?rhel} == 6
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/modules/
install -pm 755 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules/bbswitch.modules
%endif

%pre
dkms remove -m %{module} -v %{version} --rpm_safe_upgrade --all &>/dev/null
exit 0

%post
/sbin/rmmod bbswitch >/dev/null 2>&1 || :
/usr/sbin/dkms add -m %{module} -v %{version} --rpm_safe_upgrade >/dev/null 2>&1 || :
/usr/sbin/dkms build -m  %{module} -v %{version} --rpm_safe_upgrade >/dev/null 2>&1 || :
/usr/sbin/dkms install -m %{module} -v %{version} --rpm_safe_upgrade >/dev/null 2>&1 || :
exit 0

%preun
# Remove all versions from DKMS registry
dkms remove -m %{module} -v %{version} --rpm_safe_upgrade --all >/dev/null 2>&1 || :
exit 0

%postun



%files

%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/COPYING
%doc %{_docdir}/%{name}/NEWS
%doc %{_docdir}/%{name}/README.md
%{_prefix}/src/%{module}-%{version}
%if 0%{?fedora:1} || 0%{?rhel} >= 7
%{_sysconfdir}/modules-load.d/bbswitch.conf
%endif
%if 0%{?rhel} == 6
%{_sysconfdir}/sysconfig/modules/bbswitch.modules
%endif

%changelog
* Wed Jul 13 2022 Gary Gatling <gsgatlin@ncsu.edu> - 0.8.0-5
- add kernel 5.18 patch.
* Tue Apr 28 2020 Gary Gatling <gsgatlin@ncsu.edu> - 0.8.0-4
- add kernel 5.6 patch.
* Fri Aug 4 2017 Gary Gatling <gsgatlin@ncsu.edu> - 0.8.0-3
- add kernel 4.12 patch.
- add pre section to fix upgrade bug.
- add /etc/modules-load.d/bbswitch.conf to try to make sure 
  module always gets loaded at boot.
- add /etc/sysconfig/modules/bbswitch.modules on RHEL 6
  to try to make sure module always gets loaded at boot.

* Mon Feb 17 2014 Gary Gatling <gsgatlin@ncsu.edu> - 0.8.0-2
- Completely re-work package. Now called bbswitch-dkms.
- Ideas taken from the Mandriva DKMS OpenAFS package


