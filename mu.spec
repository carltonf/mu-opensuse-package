# vim: set sw=4 ts=4 et nu:

%if 0%{?suse_version} >= 1140
%define with_mug 1
%else
%define with_mug 0
%endif

%if 0%{?suse_version} >= 1210
%define with_guile 1
%else
%define with_guile 0
%endif

%define build_mu4e 1

Name:               mu
Version:            0.9.9.5
%define soname      0
Release:            1
Summary:            Maildir Email Search and Indexing
Source:             http://mu0.googlecode.com/files/mu-%{version}.tar.gz
Source1:            mug.desktop
Source2:            mug.png
Source3:            mu.sh
Patch1:             mu-mug-DATADIR.patch
Source99:           mu-rpmlintrc
URL:                http://www.djcbsoftware.nl/code/mu/
Group:              Productivity/Networking/Email/Utilities
License:            GPL-3.0+
BuildRoot:          %{_tmppath}/build-%{name}-%{version}
%if %with_mug
BuildRequires:      gtk3-devel
BuildRequires:      libwebkit-devel
%endif
%if %with_guile
BuildRequires:      guile-devel
%endif
%if 0%{?suse_version} < 1210
BuildRequires:      gmime-2_4-devel
%else
BuildRequires:      gmime-devel
%endif
BuildRequires:      glib2-devel
BuildRequires:      libxapian-devel
BuildRequires:      libuuid-devel
BuildRequires:      xdg-utils
BuildRequires:      gcc-c++ make glibc-devel pkgconfig
BuildRequires:      autoconf automake libtool
BuildRequires:      update-desktop-files
Requires:           xdg-utils
Provides:           maildir-utils = %{version}
Provides:           muile = %{version}
Obsoletes:          muile < %{version}
Obsoletes:          mu4e < %{version}

%description
Given the enormous amounts of e-mail many people gather, and the importance of
e-mail message in our work-flows, it's essential to quickly deal with all that
mail - in particular, to instantly find that one important e-mail you need
right now.

mu is a tool for dealing with e-mail messages stored in the Maildir-format. mu
main purpose is to help you to quickly find the messages you need; in addition,
it allows you to quickly to view messages, extract attachments, create new
maildirs, ...
See the mu cheatsheet for some examples.

Searching works by first indexing your messages into a Xapian-database. After
that, you can quickly find message using a powerful query language.

%if %with_guile
%package -n mu-guile
Summary:            Guile bindings for mu
Group:              System/Libraries
Obsoletes:          muile < %{version}
Requires(post):     info
Requires(preun):    info

%description -n mu-guile
mu is a tool for dealing with e-mail messages stored in the Maildir-format. mu
main purpose is to help you to quickly find the messages you need; in addition,
it allows you to quickly to view messages, extract attachments, create new
maildirs, ...

This package provides Guile bindings to the mu library.
%endif

%if %with_mug
%package -n mug
Summary:            Maildir Email Search and Indexing GUI
Requires:           mu = %{version}

%description -n mug
e-mail message in our work-flows, it's essential to quickly deal with all that
mail - in particular, to instantly find that one important e-mail you need
right now.

mu is a tool for dealing with e-mail messages stored in the Maildir-format. mu
main purpose is to help you to quickly find the messages you need; in addition,
it allows you to quickly to view messages, extract attachments, create new
maildirs, ...
See the mu cheatsheet for some examples.

Searching works by first indexing your messages into a Xapian-database. After
that, you can quickly find message using a powerful query language.

Mug is a GUI for mu.
%endif

%if %build_mu4e
%package -n mu4e
Summary:            an e-mail client for emacs with mu as backend
Requires:           emacs
Group:              System/Libraries

%description -n mu4e
Through mu, mu4e sits on top of your Maildir (which you update with e.g.
offlineimap or fetchmail). mu4e is designed to enable super-efficient handling
of e-mail; searching, reading, replying, moving, deleting. The overall 'feel' is
a bit of a mix of dired and Wanderlust.

mu4e enable utilizing mu from within Emacs.
%endif # build_mu4e


%prep
%setup -q
%patch1

%build
%configure \
%if %with_mug
    --with-gui=gtk3
%else
    --with-gui=none
%endif

%__make %{?_smp_flags} V=1 \
    DATADIR="%{_datadir}/mug"

%install
%makeinstall

%__rm -f "%{buildroot}%{_libdir}"/libguile-mu.{a,la}

%__install -D -m0644 "%{SOURCE3}" "%{buildroot}/etc/bash_completion.d/%{name}.sh"

%if %with_mug
%__install -D -m0755 toys/mug/mug "%{buildroot}%{_bindir}/mug"
%__install -D -m0644 "%{SOURCE1}" "%{buildroot}%{_datadir}/applications/mug.desktop"
%__install -D -m0644 "%{SOURCE2}" "%{buildroot}%{_datadir}/pixmaps/mug.png"
%__install -D -m0644 toys/mug/mug.svg \
    "%{buildroot}%{_datadir}/mug/mug.svg"

%suse_update_desktop_file -r mug Network Email
%else
%__rm -f "%{buildroot}%{_mandir}/man1"/mug.1*
%endif

%check
%__make test

%if %with_guile
%post   -n mu-guile
/sbin/ldconfig
%install_info --info-dir="%{_infodir}" "%{_infodir}/mu-guile.info".*

%postun -n mu-guile
/sbin/ldconfig
%install_info_delete --info-dir="%{_infodir}" "%{_infodir}/mu-guile.info".*
%endif

%if %build_mu4e
%post   -n mu4e
/sbin/ldconfig
%install_info --info-dir="%{_infodir}" "%{_infodir}/mu4e.info" .*

%postun -n mu4e
/sbin/ldconfig
%install_info_delete --info-dir="%{_infodir}" "%{_infodir}/mu4e.info" .*
%endif #


%clean
%{?buildroot:%__rm -rf "%{buildroot}"}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING HACKING NEWS TODO
%config /etc/bash_completion.d/%{name}.sh
%{_bindir}/mu
%doc %{_mandir}/man1/mu.1%{ext_man}
%doc %{_mandir}/man1/mu-*.1%{ext_man}
%doc %{_mandir}/man5/mu-*.5%{ext_man}

%if %with_guile
%files -n mu-guile
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libguile-mu.so.%{soname}
%{_libdir}/libguile-mu.so.%{soname}.*
%{_libdir}/libguile-mu.so
%dir %{_datadir}/guile/site/*.*
%{_datadir}/guile/site/*.*/mu.scm
%{_datadir}/guile/site/*.*/mu
%doc %{_infodir}/mu-guile.info*
%endif

%if %with_mug
%files -n mug
%defattr(-,root,root)
%{_bindir}/mug
%{_datadir}/mug
%{_datadir}/applications/mug.desktop
%{_datadir}/pixmaps/mug.png
%doc %{_mandir}/man1/mug.1%{ext_man}
%endif

%if %build_mu4e
%files -n mu4e
%defattr(-,root,root)
%{_datadir}/emacs/site-lisp/mu4e/*
%endif # mu4e

%changelog
