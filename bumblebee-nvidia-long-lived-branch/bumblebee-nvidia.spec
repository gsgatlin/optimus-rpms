%define bumblebee_nvidia_ver 390.42
%global debug_package %{nil}

Summary: NVIDIA's proprietary display driver installed for Bumblebee
Name: bumblebee-nvidia
Version: %{bumblebee_nvidia_ver}
Release: 1%{?dist}
License: Redistributable, no modification permitted
Group: System Environment/Base
Source0: ftp://download.nvidia.com/XFree86/Linux-x86/%{bumblebee_nvidia_ver}/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run
Source1: ftp://download.nvidia.com/XFree86/Linux-x86_64/%{bumblebee_nvidia_ver}/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run
Source2: bumblebee-nvidia
Source3: bumblebee-nvidia-fedora.te
Source4: blacklist-nvidia.conf
Source5: bumblebee-nvidia.service
Source6: bumblebee-nvidia.svinit
Source7: bumblebee-nvidia.conf-32
Source8: bumblebee-nvidia.conf-64
Source9: bumblebee-nvidia-sign.conf
Source10: bumblebee-nvidia-RHEL7.te
#Source11: 41411.patch
# Nvidia installer 361.28 https://github.com/NVIDIA/nvidia-installer/commit/1e378a81ceeb06c5899f9c7bfc8dc2f46c52a446
# Nvidia installer 361.45.11 https://github.com/NVIDIA/nvidia-installer/commit/bdbd855f007f8a1bd36bbafa299a4dff6fd3b9f8
# Nvidia installer 367.27 https://github.com/NVIDIA/nvidia-installer/commit/349a24fc329abe3ee3d471588b896b9c6b60303a
# Nvidia installer 367.44 https://github.com/NVIDIA/nvidia-installer/commit/80df9b732091f317d006a8a8daff347af69c9b6a
# Nvidia installer 367.57 https://github.com/NVIDIA/nvidia-installer/commit/9eed8858765a2d34092726c0bac6d56e7d846ea5
# To re-create:
# git clone https://github.com/NVIDIA/nvidia-installer.git
# cd nvidia-installer
# git reset --hard 9eed8858765a2d34092726c0bac6d56e7d846ea5
# cd ..
# tar -cvzf nvidia-installer.tar.gz nvidia-installer
# Repeat for new versions with different args to  "git reset --hard" and different URLs to get these args.
# Github (nvidia-installer program source code branches) can be searched.
# You may need to re-create the patch (nvidia-installer-fedorafix.patch) If they change a lot of the code.

#Source10: nvidia-installer.tar.gz

#Source9: 4.0.patch

#Patch0:         nvidia-installer-fedorafix.patch


# To re-create the sources, NVIDIA-Linux-x86_64-*.run can be downloaded from
# http://www.nvidia.com/object/unix.html Also, a copy of the script 
# bumblebee-nvidia may be obtained from https://paste.fedoraproject.org/372710/46462622/
# I release the shell script (bumblebee-nvidia) into the public domain.
# bumblebee-nvidia.te is a SELinux policy module from https://paste.fedoraproject.org/372709/62610214/
# The SELinux policy module is also released to the public domain. It is only
# required on newer fedora systems.

BuildRoot: %{_tmppath}/%{name}-root
%if 0%{?fedora} >=15 || 0%{?rhel} >= 7
Requires: selinux-policy-devel
BuildRequires: systemd-units
# Turns out 32 bit CentOS 7 doesn't have a kernel-PAE-devel!
%if 0%{?fedora:1}
%if 0%{?__isa_bits} == 32
Requires: kernel-PAE-devel
%endif
%endif
%endif
Requires: bumblebee gcc kernel-devel make glibc-devel
%if 0%{?fedora} >=18 || 0%{?rhel} >= 7
Requires: pangox-compat 
%endif
Requires:        patch

# some users need this to get it to compile.
Requires:        elfutils-libelf-devel

#BuildRequires:   libpciaccess-devel
#BuildRequires:   kmod-devel
#BuildRequires:   ncurses-devel


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

#%setup -T -b 10 -q -n nvidia-installer

#%patch0 -p1 -b .fedorafix

rm -rf $RPM_BUILD_DIR/NVIDIA-Linux-*.run
%if 0%{?__isa_bits} == 64
install -m 644 $RPM_SOURCE_DIR/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run $RPM_BUILD_DIR/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run
%else
install -m 644 $RPM_SOURCE_DIR/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run $RPM_BUILD_DIR/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run
%endif
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia $RPM_BUILD_DIR/bumblebee-nvidia

#install -m 644 $RPM_SOURCE_DIR/nvidia-unload.conf $RPM_BUILD_DIR/nvidia-unload.conf

%if 0%{?fedora} >=15
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia-fedora.te $RPM_BUILD_DIR/bumblebee-nvidia.te
%endif

%if  0%{?rhel} >= 7
install -m 644 $RPM_SOURCE_DIR/bumblebee-nvidia-RHEL7.te $RPM_BUILD_DIR/bumblebee-nvidia.te
%endif

install -m 644 $RPM_SOURCE_DIR/blacklist-nvidia.conf $RPM_BUILD_DIR/blacklist-nvidia.conf
#%if 0%{?fedora:1}
#install -m 644 %{SOURCE11}  $RPM_BUILD_DIR/41411.patch
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

#make
#Nothing to do here folks...

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/nvidia

# No longer needed...
#install -pm 644 $RPM_BUILD_DIR/nvidia-installer/_out/Linux_*/nvidia-installer $RPM_BUILD_ROOT/etc/sysconfig/nvidia
%if 0%{?__isa_bits} == 64
install -pm 644 $RPM_BUILD_DIR/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run $RPM_BUILD_ROOT/etc/sysconfig/nvidia/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run
%else
install -pm 644 $RPM_BUILD_DIR/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run $RPM_BUILD_ROOT/etc/sysconfig/nvidia/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run
%endif
mkdir -p $RPM_BUILD_ROOT/usr/sbin/
install -pm 644 $RPM_BUILD_DIR/bumblebee-nvidia $RPM_BUILD_ROOT/usr/sbin/bumblebee-nvidia

mkdir -p $RPM_BUILD_ROOT/etc/bumblebee
install -pm 644 $RPM_BUILD_DIR/bumblebee-nvidia.conf $RPM_BUILD_ROOT/etc/bumblebee/bumblebee-nvidia.conf
mkdir -p $RPM_BUILD_ROOT/etc/modprobe.d/
install -pm 644 $RPM_BUILD_DIR/blacklist-nvidia.conf $RPM_BUILD_ROOT/etc/modprobe.d/blacklist-nvidia.conf
#install -pm 644 $RPM_BUILD_DIR/nvidia-unload.conf $RPM_BUILD_ROOT/etc/modprobe.d/nvidia-unload.conf

# Example of how to use the patch function for the blob when it becomes necessary. (Which it will)
#%if 0%{?fedora:1}
#install -pm 644 $RPM_BUILD_DIR/41411.patch $RPM_BUILD_ROOT/etc/sysconfig/nvidia/41411.patch
#%endif

# systemd is a replacement for SysVinit/upstart beginning with fedora 15.

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
%if 0%{?__isa_bits} == 64
/etc/sysconfig/nvidia/NVIDIA-Linux-x86_64-%{bumblebee_nvidia_ver}.run
%else
/etc/sysconfig/nvidia/NVIDIA-Linux-x86-%{bumblebee_nvidia_ver}.run
%endif
%attr(755, root, root) /usr/sbin/bumblebee-nvidia

#%attr(755, root, root) %{_sysconfdir}/sysconfig/nvidia/nvidia-installer

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

#%if 0%{?fedora:1}
#/etc/sysconfig/nvidia/41411.patch
#%endif

%changelog
* Sat Mar 17 2018 Gary Gatling <gsgatlin@ncsu.edu> - 390.42-1
- Update to latest long lived branch version.

* Mon Jan 29 2018 Gary Gatling <gsgatlin@ncsu.edu> - 390.25-1
- remove patch for kernel  4.14.11-*.fc*.x86_64
- Update to latest long lived branch version.

* Thu Jan 04 2018 Gary Gatling <gsgatlin@ncsu.edu> - 384.98-2
- add patch for kernel >= 4.14.11-*.fc*.x86_64

* Sun Dec 10 2017 Gary Gatling <gsgatlin@ncsu.edu> - 384.98-1
- Update to latest long lived branch version.
- fix for issue with /etc/ld.so.cache.

* Sun Sep 24 2017 Gary Gatling <gsgatlin@ncsu.edu> - 384.90-1
- Update to latest long lived branch version.

* Mon Aug 28 2017 Gary Gatling <gsgatlin@ncsu.edu> - 384.69-1
- Update to latest long lived branch version.

* Thu Aug 3 2017 Gary Gatling <gsgatlin@ncsu.edu> - 384.59-1
- Update to latest long lived branch version.
- Fix SELinux problems on RHEL 7. 

* Wed May 17 2017 Gary Gatling <gsgatlin@ncsu.edu> - 375.66-1
- Update to latest long lived branch version. 

* Sun Mar 19 2017 Gary Gatling <gsgatlin@ncsu.edu> - 375.39-3
- more changes to selinux module.
- add patch for 4.10 kernel in fedora distro.
- update bumblebee-nvidia to fix flag deletions.

* Mon Feb 27 2017 Gary Gatling <gsgatlin@ncsu.edu> - 375.39-2
- update flag location to within /etc/sysconfig/nvidia/
- update selinux policy module to deal with selinux-policy-3.13.1-225.10

* Fri Feb 17 2017 Gary Gatling <gsgatlin@ncsu.edu> - 375.39-1
- Update to latest long lived branch version.
- add elfutils-libelf-devel as a dependency since some users need this for nvidia to compile.

* Fri Feb 10 2017 Gary Gatling <gsgatlin@ncsu.edu> - 375.26-2
- fix for issues caused by introduction of libglvnd to fedora 25/26.
  Added "--no-libglx-indirect --no-install-libglvnd --no-glvnd-glx-client --no-glvnd-egl-client"
  on systems with libglvnd rpm installed.

* Thu Dec 15 2016 Gary Gatling <gsgatlin@ncsu.edu> - 375.26-1
- Update to latest long lived branch version. 

* Sun Nov 20 2016 Gary Gatling <gsgatlin@ncsu.edu> - 375.20-1
- Update to latest long lived branch version. 
- Fix for https://github.com/NVIDIA/nvidia-installer/issues/1
- Fix for xorg 1.19

* Sun Oct 30 2016 Gary Gatling <gsgatlin@ncsu.edu> - 367.57-1
- Update to latest long lived branch version. (tested on 4.8.4-200 kernel)
- fix bumblebee-nvidia wrapper to not use extra args 
  (--no-symlink-check --no-runtime-check)
  if nvidia-installer does not exist in the path
  /etc/sysconfig/nvidia/nvidia-installer
- Possibly fix a problem on UEFI systems on Centos 7 / RHEL 7 version.

* Thu Aug 25 2016 Gary Gatling <gsgatlin@ncsu.edu> - 367.44-1
- Update to latest long lived branch version. (tested on 4.7 kernel)
- Update SELinux module for some fedora 24 changes.

* Thu Jun 16 2016 Gary Gatling <gsgatlin@ncsu.edu> - 367.27-1
- Update to latest long lived branch version.

* Mon May 30 2016 Gary Gatling <gsgatlin@ncsu.edu> - 361.45.11-2
- Fix issue on i686 installs, CentOS/RHEL 6/7, although...
  You REALLY should be using 64 bit installs ALWAYS on optimus notebooks.
  No optimus notebooks have 32 bit CPUs.
  Run 32 bit applications on 64 bit OS by installing relevant .i686 packages.

* Sun May 29 2016 Gary Gatling <gsgatlin@ncsu.edu> - 361.45.11-1
- Upgrade to latest long lived branch version.

* Sun May 22 2016 Gary Gatling <gsgatlin@ncsu.edu> - 361.42-2
- remove /etc/modprobe.d/nvidia-unload.conf. Problem was in bumblebee rpm.
- Update SELinux module for fedora 24 changes.

* Wed May 18 2016 Gary Gatling <gsgatlin@ncsu.edu> - 361.42-1
- Upgrade to latest long lived branch version.
- Compile + patch "nvidia-installer" ourself due to 
  https://github.com/NVIDIA/nvidia-installer/issues/1
  Unfortunately, this kills the idea of a unmanaged
  repo until the pull request gets merged...
- add /etc/modprobe.d/nvidia-unload.conf due to:
  https://github.com/Bumblebee-Project/Bumblebee/issues/719
  (Does not seem to work however)
- add "export LC_ALL=C" (Service now ticket INC2643219)

* Tue Feb 9 2016 Gary Gatling <gsgatlin@ncsu.edu> - 361.28-1
- Upgrade to latest long lived Branch version.

* Mon Dec 14 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.63-2
- Fix for https://github.com/Bumblebee-Project/Bumblebee/issues/712
- Possible fix for:
  https://www.reddit.com/r/Fedora/comments/3vthjr/problem_with_bumblebee_on_fedora_23/

* Wed Oct 21 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.63-1
- Upgrade to latest long lived Branch version.

* Wed Oct 21 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.63-1
- Upgrade to latest long lived Branch version.

* Wed Oct 21 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.55-5
- Move bumblebee-nvidia-sign.conf at the suggestion of Fahad Alduraibi 

* Tue Oct 20 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.55-4
- add bumblebee-nvidia-sign.conf at the suggestion of Fahad Alduraibi 

* Mon Oct 19 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.55-3
- Make install more silent on first install and package removal.
- fix desktop launcher in menu system for nvidia-settings program.

* Fri Oct 16 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.55-2
- fix issue with RHEL 6

* Fri Oct 16 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.55-1
- Upgrade to latest long lived Branch version.
- Change how we set up grub for fedora 23.
- Update bumblebee-nvidia script to know about bbswitch-dkms rpm.
- Open bug report concerning 355.11 (Sorry, there is little I can do)
- https://devtalk.nvidia.com/default/topic/885657/linux/can-t-install-driver-to-work-with-bumblebee-with-version-355-11/

* Sat Oct 3 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.41-1
- Upgrade to latest long lived Branch version.

* Sun Aug 2 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.30-1
- Upgrade to latest long lived Branch version.

* Tue Jun 23 2015 Gary Gatling <gsgatlin@ncsu.edu> - 352.21-1
- Upgrade to latest long lived Branch version.
- Addition to SELINUX module for shm...

* Tue May 26 2015 Gary Gatling <gsgatlin@ncsu.edu> - 346.72-2
- fix for RHEL 6 in bumblebee-nvidia script.

* Tue May 19 2015 Gary Gatling <gsgatlin@ncsu.edu> - 346.72-1
- Upgrade to latest long lived Branch version.
- Remove 4.0 patch from fedora 22 as its not needed any longer.

* Fri Apr 03 2015 Gary Gatling <gsgatlin@ncsu.edu> - 346.47-2
- Fixes for fedora 22 alpha including a 4.0.patch file.
- Update SELINUX policy for fc22.

* Mon Mar 16 2015 Gary Gatling <gsgatlin@ncsu.edu> - 346.47-1
- Improvement to shell script to remove some warnings the
  installer was displaying with "--debug" on.
- Upgrade to latest long lived Branch version.
- Remove 3.18 patch as its no longer required.

* Mon Feb 16 2015 Gary Gatling <gsgatlin@ncsu.edu> - 346.35-3
- Changes to shell script required by 346.35 if missing
  32 bit mesa-libGL rpm.
- Try to finally fix selinux issues in fc21+...

* Thu Jan 15 2015 Gary Gatling <gsgatlin@ncsu.edu> - 346.35-2
- add patch to make it work on fedora 21 kernel 3.18.

* Thu Jan 15 2015 Gary Gatling <gsgatlin@ncsu.edu> - 346.35-1
- Upgrade to latest long lived Branch version.
- Try some more selinux stanzas in our selinux module.

* Thu Jan 15 2015 Gary Gatling <gsgatlin@ncsu.edu> - 340.65-1
- Upgrade to latest long lived Branch version.

* Wed Nov 19 2014 Gary Gatling <gsgatlin@ncsu.edu> - 340.46-4
- Some fixes for SELinux problems in fedora 21+.
- You still need to use selinux in "permissive" mode 
  due to issue #600 in fedora 21+. ("enforcing" is default in 21+)
  https://github.com/Bumblebee-Project/Bumblebee/issues/600#issuecomment-63695738

* Fri Nov 7 2014 Gary Gatling <gsgatlin@ncsu.edu> - 340.46-3
- make bumblebee-nvidia know about libGLESv2.so.2.

* Thu Oct 30 2014 Gary Gatling <gsgatlin@ncsu.edu> - 340.46-2
- Try blacklisting nouveau for fc21.

* Mon Aug 18 2014 Gary Gatling <gsgatlin@ncsu.edu> - 340.46-1
- Upgrade to latest long lived Branch version.
- Upgrade SELinux security policy for fedora 21 changes.

* Mon Aug 18 2014 Gary Gatling <gsgatlin@ncsu.edu> - 340.32-1
- Upgrade to latest long lived Branch version.

* Mon Jul 7 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.79-3
- Fix for bumblebee-nvidia.conf file.

* Thu Jul 3 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.79-2
- Make it so that there is a single src package for 32 and 64 bit.

* Thu Jun 5 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.79-1
- Upgrade to latest long lived Branch version.

* Tue May 6 2014 Gary Gatling <gsgatlin@ncsu.edu> - 334.21-3
- Change patch so that it only installs on f20 and change 
  its contents to remove rejected hunks.

* Mon May 5 2014 Gary Gatling <gsgatlin@ncsu.edu> - 334.21-2
- Upgrade to latest short lived Branch version.
- add patch to make it work on fedora.


* Mon May 5 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.67-2
- Remove patch for 3.13
- add /usr/lib64/libEGL.so.1* /usr/lib/libEGL.so.1*
  to protected files in bumblebee-nvidia script.

* Thu Apr 17 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.67-1
- Upgrade to latest long lived Branch version.

* Thu Feb 20 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.49-2
- Fix init issue in RHEL 6.
- Fix various issues in RHEL 7.

* Thu Feb 20 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.49-1
- Upgrade to newest stable version.

* Tue Feb 18 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.38-2
- Add patch for 3.13 kernel.
- Update bash wrapper.
- Update SELINUX policy.

* Sat Feb 15 2014 Gary Gatling <gsgatlin@ncsu.edu> - 331.38-1
- Upgrade to newest stable version.

* Fri Nov 15 2013 Gary Gatling <gsgatlin@ncsu.edu> - 331.20-1
- Upgrade to newest stable version.

* Thu Sep 19 2013 Gary Gatling <gsgatlin@ncsu.edu> - 319.49-1
- Upgrade to newest stable version due to 3.11 kernel.
- Side effects/bug see https://github.com/Bumblebee-Project/Bumblebee/issues/433

* Sun Aug 11 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.51-8
- Bugfix in shell script.

* Sat Aug 10 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.51-7
- Fix for fedora 18.

* Sun Jul 28 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.51-6
- Fix for RHEL 6.

* Sun Jul 28 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.51-5
- Restrict new kernel patch to fedora 19 only.

* Sun Jul 28 2013 Gilboa Davara <gilboad@gmail.com> - 310.51-4
- Added support for kernels newer then 3.10 and a mechanism 
  for adding in various patches to the blob.

* Wed Jul 24 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.51-3
- add /etc/modprobe.d/blacklist-nvidia.conf for bbswitch issue #61 on github.com

* Sun Jul 21 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.51-2
- Fix problems with script on 32 bit systems.

* Wed Jun 5 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.51-1
- Upgrade to newer stable version. 319.23 crashes X leaving nvidia unable to unload.
  Any help welcome from fedora users https://github.com/Bumblebee-Project/Bumblebee/issues/433
- Add chattr +i and chattr -i to shell script to prevent nvidia installer 
  from destroying system libraries during install and un-install on 
  etx2/3/4 filesystems.
- Fix selinux policy for fedora users.

* Sun Feb 17 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.32-7
- Add make to requires to fix bug in install on Scientific Linux.
- fix typo in shell script check mode.

* Sun Feb 17 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.32-6
- Add additional conflicts.

* Sun Feb 17 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.32-5
- Add conflicts for various nvidia packages I have discovered.

* Fri Feb 15 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.32-4
- Add "--check" option to bumblebee-nvidia shell script.

* Thu Feb 14 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.32-3
- Add Theodore Lee's nvidia patched blob for kernel 3.7.7+.

* Thu Feb 7 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.32-2
- Add Theodore Lee's nvidia patched blob for kernel 3.7.6.

* Thu Jan 24 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.32-1
- Borrowed snippets from rpmfusion package to blacklist nouveau
- add pangox-compat dependency for fedora 18 only.
- Upgrade driver.

* Wed Jan 16 2013 Gary Gatling <gsgatlin@ncsu.edu> - 310.19-3
- Fix problem with primus library.

* Sun Dec 23 2012 Gary Gatling <gsgatlin@ncsu.edu> - 310.19-2
- Fix bug in shell script so driver will be rebuilt if needed.

* Sat Dec 22 2012 Gary Gatling <gsgatlin@ncsu.edu> - 310.19-1
- Upgrade driver.
- Fix bug in shell script for preserving system libraries.

* Wed Dec 19 2012 Gary Gatling <gsgatlin@ncsu.edu> - 304.64-2
- Upgrade shell script for f18.

* Wed Nov 14 2012 Gary Gatling <gsgatlin@ncsu.edu> - 304.64-1
- Upgrade driver.

* Mon Oct 15 2012 Gary Gatling <gsgatlin@ncsu.edu> - 304.51-2
- Fix script to work with new version.

* Mon Oct 15 2012 Gary Gatling <gsgatlin@ncsu.edu> - 304.51-1
- Upgrade driver.

* Sat May 19 2012 Gary Gatling <gsgatlin@ncsu.edu> - 295.53-1
- Upgrade driver.

* Mon May 7 2012 Gary Gatling <gsgatlin@ncsu.edu> - 295.49-1
- Upgrade driver.

* Mon May 7 2012 Gary Gatling <gsgatlin@ncsu.edu> - 295.40-1
- Initial build of a bumblebee-nvidia rpm suitable (?) for a fedora/RHEL 
  or RHEL/clone. I admit this is kind of a hack... But its better than nothing.

