%define realname ElectricFence

Summary: A debugger which detects memory allocation violations
Name: electricfence
Version: 2.2.2
Release: %mkrel 1
License: GPLv2
Group: Development/Other
URL: http://perens.com/FreeSoftware/ElectricFence/

# ftp://ftp.perens.com/pub/ElectricFence/beta/ used to be here, but
# the site is inaccessible as of lately
Source: %{realname}-%{version}.tar.gz
Patch1: ElectricFence-2.0.5-longjmp.patch
Patch2: ElectricFence-2.1-vaarg.patch
Patch3: ElectricFence-2.2.2-pthread.patch
Patch4: ElectricFence-2.2.2-madvise.patch
Patch5: ElectricFence-mmap-size.patch
Patch6: ElectricFence-2.2.2-banner.patch
Patch7: ElectricFence-2.2.2-ef.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ElectricFence is a utility for C programming and
debugging. ElectricFence uses the virtual memory hardware of your
system to detect when software overruns malloc() buffer boundaries,
and/or to detect any accesses of memory released by
free(). ElectricFence will then stop the program on the first
instruction that caused a bounds violation and you can use your
favorite debugger to display the offending statement.

Install ElectricFence if you need a debugger to find malloc()
violations.

%prep
%setup -q -n %{realname}-%{version}
%patch1 -p1 -b .longjmp
%patch2 -p1 -b .vaarg
%patch3 -p1 -b .pthread
%patch4 -p1 -b .madvise
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
make CFLAGS='${RPM_OPT_FLAGS} -DUSE_SEMAPHORE -fpic'

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}{%{_bindir},%{_libdir},%{_mandir}/man3}

make	BIN_INSTALL_DIR=%{buildroot}%{_bindir} \
	LIB_INSTALL_DIR=%{buildroot}%{_libdir} \
	MAN_INSTALL_DIR=%{buildroot}%{_mandir}/man3 \
	install

echo ".so man3/efence.3" > %{buildroot}%{_mandir}/man3/libefence.3

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README CHANGES COPYING
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_mandir}/*/*
