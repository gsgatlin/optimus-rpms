# Module is built by dkms, we don't have any debuginfo at package build time
%global debug_package %{nil}
%define module bbswitch

Summary:        Linux kernel module for Bumblebee
Name:           %{module}-dkms
Version:        0.8.0
URL:            https://github.com/Bumblebee-Project/bbswitch/
Release:        2%{?dist}
License:        GPLv3
Group:          System Environment/Base
Source0:        bbswitch-0.8.tar.gz
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
install bbswitch-dkms. In addition, even with nouveau, bbswitch will work 
after a suspend whereas vga_switcharoo in the kernel might not. See:
https://github.com/Bumblebee-Project/Bumblebee/wiki/Comparison-of-PM-methods
for further information.

%prep

%setup -q -n bbswitch-0.8

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

%post
/sbin/rmmod bbswitch >/dev/null 2>&1 || :
/usr/sbin/dkms add -m %{module} -v %{version} --rpm_safe_upgrade >/dev/null 2>&1 || :
/usr/sbin/dkms build -m  %{module} -v %{version} --rpm_safe_upgrade >/dev/null 2>&1 || :
/usr/sbin/dkms install -m %{module} -v %{version} --rpm_safe_upgrade >/dev/null 2>&1 || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{module} -v %{version} --rpm_safe_upgrade --all >/dev/null 2>&1 || :

%files

%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/COPYING
%doc %{_docdir}/%{name}/NEWS
%doc %{_docdir}/%{name}/README.md
%{_prefix}/src/%{module}-%{version}

%changelog
* Mon Feb 17 2014 Gary Gatling <gsgatlin@ncsu.edu> - 0.8.0-2
- Completely re-work package. Now called bbswitch-dkms.
- Ideas taken from the Mandriva DKMS OpenAFS package


