%define bumblebee_nvidia_ver 3.1

Summary: NVIDIA's proprietary display driver installed for Bumblebee
Name: bumblebee-nvidia
Version: %{bumblebee_nvidia_ver}
Release: 1%{?dist}
License: Redistributable, no modification permitted
Group: System Environment/Base
#Source0: ftp://download.nvidia.com/XFree86/Linux-x86/%{bumblebee_nvidia_ver}/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run
#Source1: ftp://download.nvidia.com/XFree86/Linux-x86_64/%{bumblebee_nvidia_ver}/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run
Source2: bumblebee-nvidia
#Source3: bumblebee-nvidia.te
Source3: bumblebee-nvidia-fedora.te
Source4: blacklist-nvidia.conf
Source5: bumblebee-nvidia.service
Source6: bumblebee-nvidia.svinit
Source7: bumblebee-nvidia.conf-32
Source8: bumblebee-nvidia.conf-64
Source9: bumblebee-nvidia-sign.conf
Source10: bumblebee-nvidia-RHEL7.te
#Source9: 4.0.patch

BuildArch: noarch

# To re-create the sources, NVIDIA-Linux-x86_64-*.run can be downloaded from
# http://www.nvidia.com/object/unix.html Also, a copy of the script 
# bumblebee-nvidia may be obtained from http://pastebin.com/b86A8UiV
# I release the shell script (bumblebee-nvidia) into the public domain.
# bumblebee-nvidia.te is a SELinux policy module from http://pastebin.com/eFQSrdaV
# The SELinux policy module is also released to the public domain. It is only
# required on newer fedora systems.

BuildRoot: %{_tmppath}/%{name}-root
%if 0%{?fedora} >=15 || 0%{?rhel} >= 7
Requires: selinux-policy-devel
BuildRequires: systemd-units
%if 0%{?__isa_bits} == 32
Requires: kernel-PAE-devel
%endif
%endif
Requires: bumblebee gcc kernel-devel make glibc-devel
%if 0%{?fedora} >=18 || 0%{?rhel} >= 7
Requires: pangox-compat 
%endif
Requires:        patch
Conflicts:       xorg-x11-drv-nvidia-beta
Conflicts:       xorg-x11-drv-nvidia-legacy
Conflicts:       xorg-x11-drv-nvidia-71xx
Conflicts:       xorg-x11-drv-nvidia-96xx
Conflicts:       xorg-x11-drv-nvidia-173xx
Conflicts:       xorg-x11-drv-nvidia
Conflicts:       xorg-x11-drv-nvidia-libs
Conflicts:       nvidia-x11-drv-32bit
Conflicts:       nvidia-x11-drv
Conflicts:       nvidia-settings
Conflicts:       nvidia-xconfig
Conflicts:       kmod-nvidia
Provides:        nvidia-kmod-common

%description

bumblebee-nvidia is a shell script designed to automate the install of 
the nvidia binary blob in a way that won't break LibGL from mesa on the 
integrated (Intel) driver.

%prep

#rm -rf $RPM_BUILD_DIR/NVIDIA-Linux-*.run
#%if 0%{?__isa_bits} == 64
#install -m 644 $RPM_SOURCE_DIR/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run $RPM_BUILD_DIR/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run
#%else
#install -m 644 $RPM_SOURCE_DIR/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run $RPM_BUILD_DIR/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run
#%endif
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia $RPM_BUILD_DIR/bumblebee-nvidia

%if 0%{?fedora} >=15
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia-fedora.te $RPM_BUILD_DIR/bumblebee-nvidia.te
%endif

%if  0%{?rhel} >= 7
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia-RHEL7.te $RPM_BUILD_DIR/bumblebee-nvidia.te
%endif

install -m 644 $RPM_SOURCE_DIR/blacklist-nvidia.conf $RPM_BUILD_DIR/blacklist-nvidia.conf
#%if 0%{?fedora} >=22
#install -m 644 $RPM_SOURCE_DIR/4.0.patch  $RPM_BUILD_DIR/4.0.patch
#%endif
%if 0%{?fedora} >=15 || 0%{?rhel} >= 7
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia.service $RPM_BUILD_DIR/bumblebee-nvidia.service
%endif
%if 0%{?rhel} == 6
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia.svinit $RPM_BUILD_DIR/bumblebee-nvidia.svinit
%endif

%if 0%{?__isa_bits} == 64
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia.conf-64 $RPM_BUILD_DIR/bumblebee-nvidia.conf
%else
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia.conf-32 $RPM_BUILD_DIR/bumblebee-nvidia.conf
%endif

install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia-sign.conf $RPM_BUILD_DIR/bumblebee-nvidia-sign.conf

%build

#Nothing to do here folks...


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/nvidia
#%if 0%{?__isa_bits} == 64
#install -pm 644 $RPM_BUILD_DIR/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run $RPM_BUILD_ROOT/etc/sysconfig/nvidia/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run
#%else
#install -pm 644 $RPM_BUILD_DIR/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run $RPM_BUILD_ROOT/etc/sysconfig/nvidia/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run
#%endif
mkdir -p $RPM_BUILD_ROOT/usr/sbin/
install -pm 644 $RPM_BUILD_DIR/bumblebee-nvidia $RPM_BUILD_ROOT/usr/sbin/bumblebee-nvidia
mkdir -p $RPM_BUILD_ROOT/etc/bumblebee
install -pm 644 $RPM_BUILD_DIR/bumblebee-nvidia.conf $RPM_BUILD_ROOT/etc/bumblebee/bumblebee-nvidia.conf
mkdir -p $RPM_BUILD_ROOT/etc/modprobe.d/
install -pm 644 $RPM_BUILD_DIR/blacklist-nvidia.conf $RPM_BUILD_ROOT/etc/modprobe.d/blacklist-nvidia.conf

#%if 0%{?fedora} >=22
#install -pm 644 $RPM_BUILD_DIR/4.0.patch $RPM_BUILD_ROOT/etc/sysconfig/nvidia/4.0.patch
#%endif

# systemd is a replacement for SysVinit beginning with fedora 15.

%if 0%{?fedora} >=15 || 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}/
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system/
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system/multi-user.target.wants
install -m 644 $RPM_BUILD_DIR/bumblebee-nvidia.service $RPM_BUILD_ROOT/%{_unitdir}/
install -m 644 $RPM_BUILD_DIR/bumblebee-nvidia.service $RPM_BUILD_ROOT/etc/systemd/system/bumblebee-nvidia.service
#ln -s %{_unitdir}/bumblebee-nvidia.service $RPM_BUILD_ROOT/etc/systemd/system/bumblebee-nvidia.service

mkdir -p $RPM_BUILD_ROOT/usr/share/selinux/devel
install -m 644 $RPM_BUILD_DIR/bumblebee-nvidia.te $RPM_BUILD_ROOT/usr/share/selinux/devel/bumblebee-nvidia.te
%endif

%if 0%{?rhel} == 6
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
install -m 755 $RPM_BUILD_DIR/bumblebee-nvidia.svinit $RPM_BUILD_ROOT/etc/init.d/bumblebee-nvidia
%endif

mkdir -p $RPM_BUILD_ROOT/usr/lib64/nvidia-bumblebee
mkdir -p $RPM_BUILD_ROOT/usr/lib/nvidia-bumblebee
mkdir -p $RPM_BUILD_ROOT/usr/lib64/nvidia-bumblebee/xorg/modules/extensions

mkdir -p $RPM_BUILD_ROOT/etc/bumblebee/
install -m 644 $RPM_BUILD_DIR/bumblebee-nvidia-sign.conf $RPM_BUILD_ROOT/etc/bumblebee/bumblebee-nvidia-sign.conf

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post -n bumblebee-nvidia
if [ $1 = 1 ]; then
# Initial installation
%if 0%{?fedora} >=15 || 0%{?rhel} >= 7
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
/bin/systemctl enable bumblebee-nvidia.service >/dev/null 2>&1 || :
%endif

%if 0%{?rhel} == 6
/sbin/chkconfig --add bumblebee-nvidia >/dev/null 2>&1 || :
/sbin/chkconfig --level 2345 bumblebee-nvidia on >/dev/null 2>&1 || :
%endif

%if 0%{?rhel} == 6
ISGRUB1=""
if [[ -f /boot/grub/grub.conf && ! -f /boot/grub2/grub2.cfg ]] ; then
     ISGRUB1="--grub"
fi
if [ -x /sbin/grubby ] ; then
     KERNELS=`/sbin/grubby --default-kernel`
[ -z $KERNELS ] && KERNELS=`ls /boot/vmlinuz-*%{?dist}.$(uname -m)*`
for kernel in ${KERNELS} ; do
/sbin/grubby $ISGRUB1 \
--update-kernel=${kernel} \
--args='nouveau.modeset=0 rd.driver.blacklist=nouveau' \
&>/dev/null
done
fi 
%endif


%if 0%{?fedora} >20 || 0%{?rhel} >=7
if [ -f /etc/default/grub ] ; then
sed -i 's@rhgb quiet@nouveau.modeset=0 rd.driver.blacklist=nouveau rhgb quiet@' /etc/default/grub

if [ -f /boot/grub2/grub.cfg ] ; then
grub2-mkconfig -o /boot/grub2/grub.cfg >/dev/null 2>&1 || :
fi

if [ -f /boot/efi/EFI/fedora/grub.cfg ] ; then
grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg >/dev/null 2>&1 || :
fi

if [ -f /boot/efi/EFI/centos/grub.cfg ] ; then
grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg >/dev/null 2>&1 || :
fi

if [ -f /boot/efi/EFI/redhat/grub.cfg ] ; then
grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg >/dev/null 2>&1 || :
fi

fi
%endif

fi 
# end initial install...

# Force compile on upgrades...
touch /etc/sysconfig/nvidia/compile-nvidia-driver

%if 0%{?fedora} >=15 || 0%{?rhel} >= 7
cd /usr/share/selinux/devel/
/usr/bin/make ./bumblebee-nvidia.pp >/dev/null 2>&1 || :
/usr/sbin/semodule -i /usr/share/selinux/devel/bumblebee-nvidia.pp >/dev/null 2>&1 || :
%endif

%preun -n bumblebee-nvidia
if [ $1 = 0 ]; then
# Package removal, not upgrade
%if 0%{?fedora} >=15 || 0%{?rhel} >= 7
/bin/systemctl --no-reload disable bumblebee-nvidia.service >/dev/null 2>&1 || :
%endif
%if 0%{?rhel} == 6
/sbin/chkconfig --level 2345 bumblebee-nvidia off >/dev/null 2>&1 || :
/sbin/chkconfig --del bumblebee-nvidia >/dev/null 2>&1 || :
%endif

%if 0%{?rhel} == 6
ISGRUB1=""
if [[ -f /boot/grub/grub.conf && ! -f /boot/grub2/grub2.cfg ]] ; then
     ISGRUB1="--grub"
fi
if [ -x /sbin/grubby ] ; then
     KERNELS=`ls /boot/vmlinuz-*%{?dist}.$(uname -m)*`
for kernel in ${KERNELS} ; do
/sbin/grubby $ISGRUB1 \
--update-kernel=${kernel} \
--remove-args='nouveau.modeset=0 rdblacklist=nouveau rd.driver.blacklist=nouveau nomodeset' &>/dev/null
done
fi
%endif


%if 0%{?fedora} >20 || 0%{?rhel} >=7
if [ -f /etc/default/grub ] ; then
sed -i 's@nouveau.modeset=0 rd.driver.blacklist=nouveau@@' /etc/default/grub

if [ -f /boot/grub2/grub.cfg ] ; then
grub2-mkconfig -o /boot/grub2/grub.cfg >/dev/null 2>&1 || :
fi

if [ -f /boot/efi/EFI/fedora/grub.cfg ] ; then
grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg >/dev/null 2>&1 || :
fi

if [ -f /boot/efi/EFI/centos/grub.cfg ] ; then
grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg >/dev/null 2>&1 || :
fi

if [ -f /boot/efi/EFI/redhat/grub.cfg ] ; then
grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg >/dev/null 2>&1 || :
fi

fi
%endif


/usr/sbin/bumblebee-nvidia --uninstall >/dev/null 2>&1 || :

fi
# end package removal

%postun



%files -n bumblebee-nvidia
%defattr(-,root,root,-)
%config(noreplace) /etc/bumblebee/bumblebee-nvidia.conf
%dir /etc/sysconfig/nvidia
#%if 0%{?__isa_bits} == 64
#/etc/sysconfig/nvidia/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run
#%else
#/etc/sysconfig/nvidia/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run
#%endif
%attr(755, root, root) /usr/sbin/bumblebee-nvidia

%if 0%{?fedora} >=15 || 0%{?rhel} >= 7
%{_unitdir}/bumblebee-nvidia.service
/etc/systemd/system/bumblebee-nvidia.service
/usr/share/selinux/devel/bumblebee-nvidia.te
%endif
%if 0%{?rhel} == 6
/etc/init.d/bumblebee-nvidia
%endif
%dir /usr/lib64/nvidia-bumblebee
%dir /usr/lib/nvidia-bumblebee
%dir /usr/lib64/nvidia-bumblebee/xorg/modules/extensions
/etc/modprobe.d/blacklist-nvidia.conf

%config /etc/bumblebee/bumblebee-nvidia-sign.conf

#%if 0%{?fedora} >=22
#/etc/sysconfig/nvidia/4.0.patch
#%endif


%changelog

* Wed Jun 5 2019 Gary Gatling <gsgatlin@ncsu.edu> - 3.1-1
- Changes to bumblebee-nvidia script to not use glvnd flags


* Wed Dec 12 2018 Gary Gatling <gsgatlin@ncsu.edu> - 3.0-6
- Fix minor diff between managed and unmanaged scripts.

* Thu Aug 3 2017 Gary Gatling <gsgatlin@ncsu.edu> - 3.0-5
- Fix SELinux problems on RHEL 7. 

* Sun Mar 19 2017 Gary Gatling <gsgatlin@ncsu.edu> - 3.0-4
- more changes to selinux module.
- update bumblebee-nvidia to fix flag deletions.

* Mon Feb 27 2017 Gary Gatling <gsgatlin@ncsu.edu> - 3.0-3
- update flag location to within /etc/sysconfig/nvidia/
- update selinux policy module to deal with selinux-policy-3.13.1-225.10

* Fri Feb 10 2017 Gary Gatling <gsgatlin@ncsu.edu> - 3.0-2
- fix for issues caused by introduction of libglvnd to fedora 25/26.
  Added "--no-libglx-indirect --no-install-libglvnd --no-glvnd-glx-client --no-glvnd-egl-client"
  on systems with libglvnd rpm installed.

* Sun Oct 30 2016 Gary Gatling <gsgatlin@ncsu.edu> - 3.0-1
- This currently does not work for me due to
  https://github.com/NVIDIA/nvidia-installer/issues/1
- fix bumblebee-nvidia wrapper to not use extra args 
  (--no-symlink-check --no-runtime-check)
  if nvidia-installer does not exist in the path
  /etc/sysconfig/nvidia/nvidia-installer
- Possibly fix a problem on UEFI systems on Centos 7 / RHEL 7 version.


* Mon Dec 14 2015 Gary Gatling <gsgatlin@ncsu.edu> - 2.0-6
- Fix for https://github.com/Bumblebee-Project/Bumblebee/issues/712
- Possible fix for:
  https://www.reddit.com/r/Fedora/comments/3vthjr/problem_with_bumblebee_on_fedora_23/

* Tue Oct 20 2015 Gary Gatling <gsgatlin@ncsu.edu> - 2.0-5
- Move bumblebee-nvidia-sign.conf at the suggestion of Fahad Alduraibi 

* Tue Oct 20 2015 Gary Gatling <gsgatlin@ncsu.edu> - 2.0-4
- add bumblebee-nvidia-sign.conf at the suggestion of Fahad Alduraibi 

* Mon Oct 19 2015 Gary Gatling <gsgatlin@ncsu.edu> - 2.0-3
- Make install more silent on first install and package removal.
- fix desktop launcher in menu system for nvidia-settings program.

* Fri Oct 16 2015 Gary Gatling <gsgatlin@ncsu.edu> - 2.0-2
- fix issue with RHEL 6

* Fri Oct 16 2015 Gary Gatling <gsgatlin@ncsu.edu> - 2.0-1
- Change how grub setup works for fedora 23.
- Update bumblebee-nvidia script to know about bbswitch-dkms rpm.
- Please note for short lived version of driver:
- https://devtalk.nvidia.com/default/topic/885657/linux/can-t-install-driver-to-work-with-bumblebee-with-version-355-11/

* Tue Jun 23 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.0-3
- Addition to SELINUX module for shm...

* Tue May 26 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.0-2
- fix for RHEL 6 in bumblebee-nvidia script.

* Fri May 15 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.0-1
- Fork of 346.47-2. This is a unmanaged version.
  See https://github.com/Bumblebee-Project/Bumblebee/issues/659

