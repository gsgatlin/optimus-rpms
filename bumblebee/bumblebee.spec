
Summary:        Daemon managing Optimus hybrid graphics chip sets
Name:           bumblebee
Version:        3.2.1
URL:            http://bumblebee-project.org/
Release:        14%{?dist}
License:        GPLv3+
Group:          System Environment/Base
Source0:        http://www.bumblebee-project.org/%{name}-%{version}.tar.gz
Source1:        bumblebeed.svinit
Source2:        bumblebee.conf
Patch0:         %{name}-xorgwrapfix.patch
Patch1:         %{name}-f23xorgnvidiafix.patch
Patch2:         %{name}-modprobefix.patch
Patch3:         %{name}-libglvndfix.patch
Patch4:         %{name}-boguserror.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libbsd-devel
BuildRequires:  glib2-devel
BuildRequires:  libX11-devel
BuildRequires:  help2man
%if 0%{?fedora:1} || 0%{?rhel} >= 7
BuildRequires:  kmod-devel
%endif
# In bumblebee 4.X we shall require bumblebee-bridge instead 
# of VirtualGL to give the end user more choice.
# Requires VirtualGL-2.3.2-5 or newer or recent
# ( < 0.3.05042013) primus package to work.
#Requires:       bumblebee-bridge
Requires:       VirtualGL

%if 0%{?fedora:1} || 0%{?rhel} >= 7
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd-units
%endif

%description
Bumblebee daemon is a rewrite of the original Bumblebee
(https://github.com/Bumblebee-Project/Bumblebee-old)
service, providing an elegant and stable means of managing Optimus
hybrid graphics chip sets. A primary goal of this project is to not only
enable use of the discrete GPU for rendering, but also to enable
smart power management of the discrete GPU when it's not in use.

%prep

%setup -q -n %{name}-%{version}

# add in a custom red hat style sysv init script for RHEL 6.
install -m 644 %{SOURCE1} $RPM_BUILD_DIR/%{name}-%{version}/


# xorg binary moved to new path in fedora 21+
%if 0%{?fedora} >20
%patch0 -p1 -b .xorgwrapfix
%endif

%if 0%{?fedora} >22
%patch1 -p1 -b .f23fix
%endif

%patch2 -p1 -b .modprobefix

%patch3 -p1 -b .libglvndfix

%patch4 -p1 -b .boguserror

%build

%if 0%{?rhel} == 6
sed -i -e "s|2.68|2.63|g" $RPM_BUILD_DIR/%{name}-%{version}/configure.ac
autoreconf -fi
%else
autoreconf -fi
%endif

# Next line is new for 3.2.1. We need to overide debian style default settings
export CONF_PRIMUS_LD_PATH="/usr/lib/primus:/usr/lib64/primus"
export CONF_DRIVER=nouveau
%if 0%{?rhel} == 6
%configure
%else
%configure --with-udev-rules=/usr/lib/udev/rules.d
%endif


make %{?_smp_mflags} CFLAGS="%{optflags}"
 
%install
make DESTDIR=$RPM_BUILD_ROOT install


%if 0%{?rhel} == 6
mkdir -p $RPM_BUILD_ROOT/%{_initddir}

# We must make our own init script which is more compatible with Red Hat Enterprise type 
# systems like RHEL 6 or CentOS 6, etc.

install -pm 755 $RPM_BUILD_DIR/%{name}-%{version}/bumblebeed.svinit $RPM_BUILD_ROOT/%{_initddir}/bumblebeed

%else
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/
install -pm 644 scripts/systemd/bumblebeed.service $RPM_BUILD_ROOT/%{_unitdir}/
#ln -s %{_unitdir}/bumblebeed.service $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/bumblebeed.service

%endif
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/modprobe.d/
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/modprobe.d/bumblebee.conf

# bumblebee-nouveau.conf is required so that we may manipulate a symlink in case bumblebee-nvidia is installed 

cp conf/%{name}.conf $RPM_BUILD_ROOT/%{_sysconfdir}/bumblebee/%{name}-nouveau.conf
rm $RPM_BUILD_ROOT/%{_sysconfdir}/bumblebee/%{name}.conf
ln -s %{_sysconfdir}/bumblebee/%{name}-nouveau.conf $RPM_BUILD_ROOT/%{_sysconfdir}/bumblebee/%{name}.conf


%triggerin -- bumblebee-nvidia
ln -sf %{_sysconfdir}/bumblebee/%{name}-nvidia.conf %{_sysconfdir}/bumblebee/%{name}.conf
%triggerun -- bumblebee-nvidia
[ $2 = 0 ] || exit 0
ln -sf %{_sysconfdir}/bumblebee/%{name}-nouveau.conf %{_sysconfdir}/bumblebee/%{name}.conf

%post
if [ $1 -eq 1 ] ; then
# Initial installation
%if 0%{?rhel} == 6
/sbin/chkconfig --add bumblebeed >/dev/null 2>&1 || :
/sbin/chkconfig --level 2345 bumblebeed on >/dev/null 2>&1 || :
/sbin/service bumblebeed start >/dev/null 2>&1 || :
#%else
#/bin/systemctl daemon-reload >/dev/null 2>&1 || :
#/bin/systemctl enable bumblebeed.service >/dev/null 2>&1 || :
#/bin/systemctl start bumblebeed.service >/dev/null 2>&1 || :
%endif
%{_sbindir}/groupadd %{name} >/dev/null 2>&1 || :
for user in `cat %{_sysconfdir}/passwd | grep /home | cut -d: -f1`; do
  %{_sbindir}/usermod -a -G %{name} $user >/dev/null 2>&1 || :
done
fi
%if 0%{?rhel} == 6
/sbin/service bumblebeed restart >/dev/null 2>&1 || :
%else
#%systemd_post bumblebeed.service
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
/bin/systemctl enable bumblebeed.service >/dev/null 2>&1 || :
/bin/systemctl start bumblebeed.service >/dev/null 2>&1 || :
%endif


%preun
# Package removal, not upgrade
%if 0%{?rhel} == 6
if [ $1 -eq 0 ] ; then
/sbin/service bumblebeed stop >/dev/null 2>&1 || :
/sbin/chkconfig --level 2345 bumblebeed off >/dev/null 2>&1 || :
/sbin/chkconfig --del bumblebeed >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora:1} || 0%{?rhel} >= 7
%systemd_preun bumblebeed.service
%endif


%postun
%if 0%{?fedora:1} || 0%{?rhel} >= 7
%systemd_postun_with_restart bumblebeed.service
%endif


%files
%dir %{_sysconfdir}/%{name}
%doc %{_docdir}/%{name}/README.markdown
%doc %{_docdir}/%{name}/RELEASE_NOTES_3_2_1
%{_mandir}/man1/bumblebeed.1.gz
%{_mandir}/man1/optirun.1.gz
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-nouveau.conf
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/xorg.conf.nouveau
%config(noreplace) %{_sysconfdir}/%{name}/xorg.conf.nvidia
%{_bindir}/%{name}-bugreport
%{_bindir}/optirun
%{_sbindir}/bumblebeed
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/xorg.conf.d/10-dummy.conf
%if 0%{?rhel} == 6
%{_initddir}/bumblebeed
/lib/udev/rules.d/99-bumblebee-nvidia-dev.rules

%else
%{_unitdir}/bumblebeed.service
#%{_sysconfdir}/systemd/system/bumblebeed.service
%{_prefix}/lib/udev/rules.d/99-bumblebee-nvidia-dev.rules
%endif
%{_sysconfdir}/modprobe.d/bumblebee.conf

%changelog
* Wed Aug 1 2018 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-14
- add bumblebee-boguserror.patch for
- https://github.com/Bumblebee-Project/Bumblebee/issues/974

* Fri Feb 10 2017 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-13
- Add bumblebee-libglvndfix.patch because of addition of libglvnd
  to fedora 26 and possibly fedora 25.

* Wed Jun 22 2016 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-12
- redo modprobe patch. (slight mess up in logging)

* Thu Jun 16 2016 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-11
- redo modprobe patch for nvidia 367.27.

* Tue May 24 2016 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-10
- Add patch for "rmmod" to "modeprobe -r".
- Fix somne problems with service being enabled by default in fc24.

* Tue Oct 13 2015 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-9
- Add patch for xorg.conf.nvidia in fedora 23.

* Tue Oct 13 2015 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-8
- Make sure default config file uses nouveau driver.
  For nvidia a different file is used

* Mon Jan 19 2015 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-7
- Bruno Pagani has asked that /etc/modprobe.d/bumblebee.conf
  be added in gihub issue 582:
  https://github.com/Bumblebee-Project/Bumblebee/issues/582
  to blacklist nvidia and nouveau modules.

* Sun Nov 9 2014 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-6
- Fix xorg binary path for fedora 21+ via patch.

* Mon Jul 7 2014 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-5
- Fix missing build require for mockbuild process. ( systemd-units )

* Mon Jul 29 2013 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-4
- Reverted some changes for now so the service can auto-startup.

* Fri Jul 26 2013 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-3
- Made changes to better follow packaging guidelines.
- To fix problems with the previous version, type
  rpm -e --noscripts bumblebee-3.2.1-2
  rpm -e bumblebee --nodeps
  yum install bumblebee

* Wed Jul 24 2013 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-2
- Made changes to better follow packaging guidelines.

* Sun May 12 2013 Gary Gatling <gsgatlin@ncsu.edu> - 3.2.1-1
- Upgrade to version 3.2.1

* Mon Feb 25 2013 Gary Gatling <gsgatlin@ncsu.edu> - 3.1-1
- Upgrade to version 3.1

* Thu Feb 07 2013 Theodore Lee <theo148@gmail.com> - 3.0.1-2
- Add workaround patch for issue with deprecated "rmmod --wait" option
- Add missing BuildRequires for autoconf, automake, and libX11-devel

* Mon Aug 13 2012 Gary Gatling <gsgatlin@ncsu.edu> - 3.0.1-1
- Upgrade to 3.0.1. bugfixes including a fix for a critical bug affecting new Kepler-based laptops 

* Sun Aug 5 2012 Gary Gatling <gsgatlin@ncsu.edu> - 3.0.0-3
- Added stack smashing fix patch. 
- Made further changes to specfile.

* Sun Jun 10 2012 Gary Gatling <gsgatlin@ncsu.edu> - 3.0.0-2
- Made first round of changes to better follow packaging guidelines.

* Wed May 16 2012 Gary Gatling <gsgatlin@ncsu.edu> - 3.0.0-1
- Initial build of a bumblebee rpm for fedora or RHEL6/clone.

