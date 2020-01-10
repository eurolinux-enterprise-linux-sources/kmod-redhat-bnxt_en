%define kmod_name		bnxt_en
%define kmod_vendor		redhat
%define kmod_driver_version	1.10.0_dup7.7
%define kmod_driver_epoch	%{nil}
%define kmod_rpm_release	1
%define kmod_kernel_version	3.10.0-1062.el7
%define kmod_kernel_version_min	%{nil}
%define kmod_kernel_version_dep	%{nil}
%define kmod_kbuild_dir		drivers/net/ethernet/broadcom/bnxt
%define kmod_dependencies       %{nil}
%define kmod_dist_build_deps	%{nil}
%define kmod_build_dependencies	%{nil}
%define kmod_devel_package	0
%define kmod_install_path	extra/kmod-redhat-bnxt_en
%define kernel_pkg		kernel
%define kernel_devel_pkg	kernel-devel
%define kernel_modules_pkg	kernel-modules

%{!?dist: %define dist .el7_7}
%{!?make_build: %define make_build make}

%if "%{kmod_kernel_version_dep}" == ""
%define kmod_kernel_version_dep %{kmod_kernel_version}
%endif

%if "%{kmod_dist_build_deps}" == ""
%if (0%{?rhel} > 7) || (0%{?centos} > 7)
%define kmod_dist_build_deps redhat-rpm-config kernel-abi-whitelists elfutils-libelf-devel kernel-rpm-macros kmod
%else
%define kmod_dist_build_deps redhat-rpm-config kernel-abi-whitelists
%endif
%endif

Source0:	%{kmod_name}-%{kmod_vendor}-%{kmod_driver_version}.tar.bz2
# Source code patches
Patch0:	0000-bump-version.patch
Patch1:	0001-netdrv-bnxt_en-Add-support-for-BCM957504.patch
Patch2:	_PATCH_RHEL7_1-7_bnxt_en_Add_device_IDs_0x1806_and_0x1752_for_57500_de.patch
Patch3:	_PATCH_RHEL7_2-7_bnxt_en_Add_PCI_IDs_for_57500_series_NPAR_devices.patch
Patch4:	_PATCH_RHEL-7_01-12_bnxt_en_Improve_RX_consumer_index_validity_check.patch
Patch5:	_PATCH_RHEL-7_02-12_bnxt_en_Reset_device_on_RX_buffer_errors.patch
Patch6:	_PATCH_RHEL-7_03-12_bnxt_en_Improve_multicast_address_setup_logic.patch
Patch7:	_PATCH_RHEL-7_04-12_bnxt_en_Free_short_FW_command_HWRM_memory_in_error.patch
Patch8:	_PATCH_RHEL-7_05-12_bnxt_en_Fix_possible_crash_in_bnxt_hwrm_ring_free_.patch
Patch9:	_PATCH_RHEL-7_06-12_bnxt_en_Pass_correct_extended_TX_port_statistics_s.patch
Patch10:	_PATCH_RHEL-7_07-12_bnxt_en_Fix_statistics_context_reservation_logic.patch
Patch11:	_PATCH_RHEL-7_08-12_bnxt_en_Fix_uninitialized_variable_usage_in_bnxt_r.patch
Patch12:	_PATCH_RHEL-7_09-12_bnxt_en_Improve_NQ_reservations.patch
Patch13:	_PATCH_RHEL-7_10-12_bnxt_en_Fix_aggregation_buffer_leak_under_OOM_cond.patch
Patch14:	_PATCH_RHEL-7_11-12_bnxt_en_Fix_possible_BUG__condition_when_calling_p.patch
Patch15:	_PATCH_RHEL-7_12-12_bnxt_en_Reduce_memory_usage_when_running_in_kdump_.patch
Patch16:	_PATCH_RHEL7_3-7_bnxt_en_Disable_bus_master_during_PCI_shutdown_and_dr.patch
Patch17:	_PATCH_RHEL7_4-7_bnxt_en_Suppress_error_messages_when_querying_DSCP_DC.patch
Patch18:	_PATCH_RHEL7_5-7_bnxt_en_Cap_the_returned_MSIX_vectors_to_the_RDMA_dri.patch
Patch19:	_PATCH_RHEL7_6-7_bnxt_en_Fix_statistics_context_reservation_logic_for_.patch
Patch20:	_PATCH_RHEL7_7-7_bnxt_en_Fix_ethtool_selftest_crash_under_error_condit.patch

%define findpat %( echo "%""P" )
%define __find_requires /usr/lib/rpm/redhat/find-requires.ksyms
%define __find_provides /usr/lib/rpm/redhat/find-provides.ksyms %{kmod_name} %{?epoch:%{epoch}:}%{version}-%{release}
%define sbindir %( if [ -d "/sbin" -a \! -h "/sbin" ]; then echo "/sbin"; else echo %{_sbindir}; fi )
%define dup_state_dir %{_localstatedir}/lib/rpm-state/kmod-dups
%define kver_state_dir %{dup_state_dir}/kver
%define kver_state_file %{kver_state_dir}/%{kmod_kernel_version}.%(arch)
%define dup_module_list %{dup_state_dir}/rpm-kmod-%{kmod_name}-modules

Name:		kmod-redhat-bnxt_en
Version:	%{kmod_driver_version}
Release:	%{kmod_rpm_release}%{?dist}
%if "%{kmod_driver_epoch}" != ""
Epoch:		%{kmod_driver_epoch}
%endif
Summary:	bnxt_en kernel module for Driver Update Program
Group:		System/Kernel
License:	GPLv2
URL:		https://www.kernel.org/
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	%kernel_devel_pkg = %kmod_kernel_version
%if "%{kmod_dist_build_deps}" != ""
BuildRequires:	%{kmod_dist_build_deps}
%endif
ExclusiveArch:	x86_64
%global kernel_source() /usr/src/kernels/%{kmod_kernel_version}.$(arch)

%global _use_internal_dependency_generator 0
%if "%{?kmod_kernel_version_min}" != ""
Provides:	%kernel_modules_pkg >= %{kmod_kernel_version_min}.%{_target_cpu}
%else
Provides:	%kernel_modules_pkg = %{kmod_kernel_version_dep}.%{_target_cpu}
%endif
Provides:	kmod-%{kmod_name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(post):	%{sbindir}/weak-modules
Requires(postun):	%{sbindir}/weak-modules
Requires:	kernel >= 3.10.0-1062.el7

Requires:	kernel < 3.10.0-1063.el7
%if 0
Requires: firmware(%{kmod_name}) = ENTER_FIRMWARE_VERSION
%endif
%if "%{kmod_build_dependencies}" != ""
BuildRequires:  %{kmod_build_dependencies}
%endif
%if "%{kmod_dependencies}" != ""
Requires:       %{kmod_dependencies}
%endif
# if there are multiple kmods for the same driver from different vendors,
# they should conflict with each other.
Conflicts:	kmod-%{kmod_name}

%description
bnxt_en kernel module for Driver Update Program

%if 0

%package -n kmod-redhat-bnxt_en-firmware
Version:	ENTER_FIRMWARE_VERSION
Summary:	bnxt_en firmware for Driver Update Program
Provides:	firmware(%{kmod_name}) = ENTER_FIRMWARE_VERSION
%if "%{kmod_kernel_version_min}" != ""
Provides:	%kernel_modules_pkg >= %{kmod_kernel_version_min}.%{_target_cpu}
%else
Provides:	%kernel_modules_pkg = %{kmod_kernel_version_dep}.%{_target_cpu}
%endif
%description -n  kmod-redhat-bnxt_en-firmware
bnxt_en firmware for Driver Update Program


%files -n kmod-redhat-bnxt_en-firmware
%defattr(644,root,root,755)
%{FIRMWARE_FILES}

%endif

# Development package
%if 0%{kmod_devel_package}
%package -n kmod-redhat-bnxt_en-devel
Version:	%{kmod_driver_version}
Requires:	kernel >= 3.10.0-1062.el7

Requires:	kernel < 3.10.0-1063.el7
Summary:	bnxt_en development files for Driver Update Program

%description -n  kmod-redhat-bnxt_en-devel
bnxt_en development files for Driver Update Program


%files -n kmod-redhat-bnxt_en-devel
%defattr(644,root,root,755)
/usr/share/kmod-%{kmod_vendor}-%{kmod_name}/Module.symvers
%endif

%post
modules=( $(find /lib/modules/%{kmod_kernel_version}.%(arch)/%{kmod_install_path} | grep '\.ko$') )
printf '%s\n' "${modules[@]}" | %{sbindir}/weak-modules --add-modules --no-initramfs

mkdir -p "%{kver_state_dir}"
touch "%{kver_state_file}"

exit 0

%posttrans
# We have to re-implement part of weak-modules here because it doesn't allow
# calling initramfs regeneration separately
if [ -f "%{kver_state_file}" ]; then
	kver_base="%{kmod_kernel_version_dep}"
	kvers=$(ls -d "/lib/modules/${kver_base%%.*}"*)

	for k_dir in $kvers; do
		k="${k_dir#/lib/modules/}"

		tmp_initramfs="/boot/initramfs-$k.tmp"
		dst_initramfs="/boot/initramfs-$k.img"

		# The same check as in weak-modules: we assume that the kernel present
		# if the symvers file exists.
		if [ -e "/boot/symvers-$k.gz" ]; then
			/usr/bin/dracut -f "$tmp_initramfs" "$k" || exit 1
			cmp -s "$tmp_initramfs" "$dst_initramfs"
			if [ "$?" = 1 ]; then
				mv "$tmp_initramfs" "$dst_initramfs"
			else
				rm -f "$tmp_initramfs"
			fi
		fi
	done

	rm -f "%{kver_state_file}"
	rmdir "%{kver_state_dir}" 2> /dev/null
fi

rmdir "%{dup_state_dir}" 2> /dev/null

exit 0

%preun
if rpm -q --filetriggers kmod 2> /dev/null| grep -q "Trigger for weak-modules call on kmod removal"; then
	mkdir -p "%{kver_state_dir}"
	touch "%{kver_state_file}"
fi

mkdir -p "%{dup_state_dir}"
rpm -ql kmod-redhat-bnxt_en-%{kmod_driver_version}-%{kmod_rpm_release}%{?dist}.$(arch) | \
	grep '\.ko$' > "%{dup_module_list}"

%postun
if rpm -q --filetriggers kmod 2> /dev/null| grep -q "Trigger for weak-modules call on kmod removal"; then
	initramfs_opt="--no-initramfs"
else
	initramfs_opt=""
fi

modules=( $(cat "%{dup_module_list}") )
rm -f "%{dup_module_list}"
printf '%s\n' "${modules[@]}" | %{sbindir}/weak-modules --remove-modules $initramfs_opt

rmdir "%{dup_state_dir}" 2> /dev/null

exit 0

%files
%defattr(644,root,root,755)
/lib/modules/%{kmod_kernel_version}.%(arch)
/etc/depmod.d/%{kmod_name}.conf
/usr/share/doc/kmod-%{kmod_name}/greylist.txt

%prep
%setup -n %{kmod_name}-%{kmod_vendor}-%{kmod_driver_version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
rm -rf obj
cp -r source obj

PWD_PATH="$PWD"
%if "%{workaround_no_pwd_rel_path}" != "1"
PWD_PATH=$(realpath --relative-to="%{kernel_source}" . 2>/dev/null || echo "$PWD")
%endif
%{make_build} -C %{kernel_source} V=1 M="$PWD_PATH/obj/%{kmod_kbuild_dir}" \
	NOSTDINC_FLAGS="-I$PWD_PATH/obj/include -I$PWD_PATH/obj/include/uapi" \
	EXTRA_CFLAGS="%{nil}" \
	%{nil}
# mark modules executable so that strip-to-file can strip them
find obj/%{kmod_kbuild_dir} -name "*.ko" -type f -exec chmod u+x '{}' +

whitelist="/lib/modules/kabi-current/kabi_whitelist_%{_target_cpu}"
for modules in $( find obj/%{kmod_kbuild_dir} -name "*.ko" -type f -printf "%{findpat}\n" | sed 's|\.ko$||' | sort -u ) ; do
	# update depmod.conf
	module_weak_path=$(echo "$modules" | sed 's/[\/]*[^\/]*$//')
	if [ -z "$module_weak_path" ]; then
		module_weak_path=%{name}
	else
		module_weak_path=%{name}/$module_weak_path
	fi
	echo "override $(echo $modules | sed 's/.*\///')" \
	     "$(echo "%{kmod_kernel_version_dep}" |
	        sed 's/\.[^\.]*$//;
		     s/\([.+?^$\/\\|()\[]\|\]\)/\\\0/g').*" \
		     "weak-updates/$module_weak_path" >> source/depmod.conf

	# update greylist
	nm -u obj/%{kmod_kbuild_dir}/$modules.ko | sed 's/.*U //' |  sed 's/^\.//' | sort -u | while read -r symbol; do
		grep -q "^\s*$symbol\$" $whitelist || echo "$symbol" >> source/greylist
	done
done
sort -u source/greylist | uniq > source/greylist.txt

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=%{kmod_install_path}
PWD_PATH="$PWD"
%if "%{workaround_no_pwd_rel_path}" != "1"
PWD_PATH=$(realpath --relative-to="%{kernel_source}" . 2>/dev/null || echo "$PWD")
%endif
make -C %{kernel_source} modules_install \
	M=$PWD_PATH/obj/%{kmod_kbuild_dir}
# Cleanup unnecessary kernel-generated module dependency files.
find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;

install -m 644 -D source/depmod.conf $RPM_BUILD_ROOT/etc/depmod.d/%{kmod_name}.conf
install -m 644 -D source/greylist.txt $RPM_BUILD_ROOT/usr/share/doc/kmod-%{kmod_name}/greylist.txt
%if 0
%{FIRMWARE_FILES_INSTALL}
%endif
%if 0%{kmod_devel_package}
install -m 644 -D $PWD/obj/%{kmod_kbuild_dir}/Module.symvers $RPM_BUILD_ROOT/usr/share/kmod-%{kmod_vendor}-%{kmod_name}/Module.symvers
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Sep 27 2019 Eugene Syromiatnikov <esyr@redhat.com> 1.10.0_dup7.7-1
- c45db7d2f34d6fad924c20443f73147dca7f6e29
- bnxt_en kernel module for Driver Update Program
- Resolves: #bz1755331
