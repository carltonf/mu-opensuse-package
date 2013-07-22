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

Name:               mu
Version:            0.9.9
%define soname      0
Release:            2.1
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
BuildRequires:      gtk2-devel
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

%prep
%setup -q
%patch1

%build
%configure \
%if %with_mug
    --with-gui=gtk2
%else
    --with-gui=none
%endif

%__make %{?_smp_flags} V=1 \
    DATADIR="%{_datadir}/mug"

%__install -D -m0644 toys/mug/mug.svg \
    "%{buildroot}%{_datadir}/mug/mug.svg"

%install
%makeinstall

%__rm -f "%{buildroot}%{_libdir}"/libguile-mu.{a,la}

%__install -D -m0644 "%{SOURCE3}" "%{buildroot}/etc/bash_completion.d/%{name}.sh"

%if %with_mug
%__install -D -m0755 toys/mug/mug "%{buildroot}%{_bindir}/mug"
%__install -D -m0644 "%{SOURCE1}" "%{buildroot}%{_datadir}/applications/mug.desktop"
%__install -D -m0644 "%{SOURCE2}" "%{buildroot}%{_datadir}/pixmaps/mug.png"
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

%changelog
* Tue Oct 16 2012 pascal.bleser@opensuse.org
- update to 0.9.9:
  * ** mu4e
  - view: address can be toggled long/short, compose message
  - sanitize opening urls (mouse-1, and not too eager)
  - tooltips for header labels, flags
  - add sort buttons to header-labels
  - support signing / decryption of messages
  - improve address-autocompletion (e.g., ensure it's case-insensitive)
  - much faster when there are many maildirs
  - improved line wrapping
  - better handle attached messages
  - improved URL-matching
  - improved messages to user (mu4e-(warn|error|message))
  - add refiling functionality
  - support fancy non-ascii in the UI
  - dynamic folders (i.e.., allow mu4e-(sent|draft|trash|refile)-folder) to
    be a function
  - dynamic attachment download folder (can be a function now)
  - much improved manual
  * ** mu
  - remove --summary (use --summary-len instead)
  - add --after for mu find, to limit to messages after T
  - add new command `mu verify', to verify signatures
  - fix iso-2022-jp decoding (and other 7-bit clean non-ascii)
  - add support for X-keywords
  - performance improvements for threaded display (~ 25%% for 23K msgs)
  - mu improved user-help (and the 'mu help' command)
  - toys/mug2 replaces toys/mug
  * ** mu-guile
  - automated tests
  - add mu:timestamp, mu:count
  - handle db reopenings in the background
- changes from 0.9.8.5:
  * ** mu4e
  - auto-completion of e-mail addresses
  - inline display of images (see `mu4e-view-show-images'), uses imagemagick
    if available
  - interactively change number of headers / columns for showing headers with
    C-+ and C-- in headers, view mode
  - support flagging message
  - navigate to previous/next queries like a web browser (with <M-left>,
    <M-right>)
  - narrow search results with '/'
  - next/previous take a prefix arg now, to move to the nth previous/next message
  - allow for writing rich-text messages with org-mode
  - enable marking messages as Flagged
  - custom marker functions (see manual)
  - better "dwim" handling of buffer switching / killing
  - deferred marking of message (i.e.., mark now, decide what to mark for
    later)
  - enable changing of sort order, display of threads
  - clearer marks for marked messages
  - fix sorting by subject (disregarding Re:, Fwd: etc.)
  - much faster handling when there are many maildirs (speedbar)
  - handle mailto: links
  - improved, extended documentation
  * ** mu
  - support .noupdate files (parallel to .noindex, dir is ignored unless we're
    doing a --rebuild).
  - append all inline text parts, when getting the text body
  - respect custom maildir flags
  - correctly handle the case where g_utf8_strdown (str) > len (str)
  - make gtk, guile, webkit dependency optional, even if they are installed
* Wed May  9 2012 pascal.bleser@opensuse.org
- update to 0.9.8.4:
  * fix for opening files with non-ascii names
  * much improved support for searching non-Latin (Cyrillic etc.) languages we
    can now match 'Тесла' or 'Аркона' without problems
  * smarter escaping (fixes issues with finding message ids)
  * fixes for queries with brackets
  * allow --summary-len for the length of message summaries
  * numerous other small fixes
* Sat Apr 14 2012 pascal.bleser@opensuse.org
- update to 0.9.8.3:
  * existing mu/mu4e are recommended to run `mu index --rebuild' after upgrade
  * mu4e:
  - allow for searching by editing bookmarks
    (`mu4e-search-bookmark-edit-first') (keybinding 'B')
  - make it configurable what to do with sent messages (see
    `mu4e-sent-messages-behavior')
  - speedbar support
  - better handling of drafts:
  - don't save too early
  - more descriptive buffer names (based on Subject, if any)
  - don't put "--text-follows-this-line--" markers in files
  - automatically include signatures, if set
  - add user-settable variables mu4e-view-wrap-lines and mu4e-view-hide-cited,
    which determine the initial way a message is displayed
  - improved documentation
  * general:
  - much improved searching for GMail folders (i.e. maildir:/ matching);
    this requires a 'mu index --rebuild'
  - correctly handle utf-8 messages, even if they don't specify this explicitly
  - fixe mu_msg_move_to_maildir for top-level messages
  - fixes in maildir scanning
  - plugs some memleaks
* Sun Mar 11 2012 pascal.bleser@opensuse.org
- update to 0.9.8.2:
  * add automatic mail update
  * add automatic handling of marked messages
  * fixes for non-UTF-8 systems
  * add symlinking messages
  * fixes some problems opening attachments
  * improved documentation
* Sat Feb 18 2012 pascal.bleser@opensuse.org
- disable guile bindings on < 12.1, guile too old (needs 2.0)
* Sat Feb 18 2012 pascal.bleser@opensuse.org
- update to 0.9.8.1:
  * show only leaf/rfc822 MIME-parts
  * mu4e:
  - allow for shell commands with arguments in `mu4e-get-mail-command'
  - support marking messages as 'read' and 'unread'
  - show the current query in the the mode-line (`global-mode-string')
  - don't repeat 'Re:' / 'Fwd:'
  - colorize cited message parts
  - better handling of text-based, embedded message attachments
  - for text-bodies, concatenate all text/plain parts
  - make filladapt dep optional
  - documentation improvements
- changes from 0.9.8:
  * '--descending' has  been renamed into '--reverse'
  * search for attachment MIME-type using 'mime:' or 'y:'
  * search for text in text-attachments using 'embed:' or 'e:'
  * searching for attachment file names now uses 'file:' (was: 'attach:')
  * experimental emacs-based mail client -- "mu4e"
  * added more unit tests
  * improved guile binding - no special binary is needed anymore, it's
    installable are works with the normal guile system; code has been
    substantially improved. still 'experimental'
* Fri Nov 11 2011 pascal.bleser@opensuse.org
- fix location for mug.svg
* Sat Sep  3 2011 pascal.bleser@opensuse.org
- build muile as a separate subpackage as it requires guile
- update to 0.9.7:
  * don't enforce UTF-8 output, use locale (fixes issue #11)
  * add mail threading to mu-find (using -t/--threads) (sorta fixes issue #13)
  * add header line to --format=mutt-ab (mu cfind), (fixes issue #42)
  * terminate mu view results with a form-feed marker (use --terminate) (fixes
    issue #41)
  * search X-Label: tags (fixes issue #40)
  * added toys/muile, the mu guile shell, which allows for message stats etc
  * fix date handling (timezones)
* Fri Jun  3 2011 pascal.bleser@opensuse.org
- dropped mu-backport_g_key_file_uint64.patch, not needed any more, fixed
  upstream
- update to 0.9.6:
  * fix matching for mu cfind to be as expected
  * fix mu-contacts for broken names/emails
  * clear the contacts-cache too when doing a --rebuild
  * wildcard searches ('*') for fields (except for path/maildir)
  * search for attachment file names (with 'a:'/'attach:') -- also works with
    wildcards
  * remove --xquery completely; use --output=xquery instead
  * fix progress info in 'mu index'
  * display the references for a message using the 'r' character (mu find)
  * remove --summary-len/-k, instead use --summary for mu view and mu find, and
    support colorized output for some sub-commands (view, cfind and extract).
    Disabled by default, use --color to enable, or set env MU_COLORS to
    non-empty
  * update documentation, added more examples
* Tue Apr 26 2011 pascal.bleser@opensuse.org
- mug only built on openSUSE >= 11.4, requires newer gtk2
- update to 0.9.5:
  * bug fix for infinite loop in Maildir detection
  * small optimizations
- changes from 0.9.4:
  * add the 'cfind' command, to search/export contact information
  * add 'flag:unread' as a synonym for 'flag:new OR NOT flag:unseen'
  * updated documentation
* Sat Feb 19 2011 pascal.bleser@opensuse.org
- remove symbolic links again, they don't work
- add bash completion
* Sat Feb 19 2011 pascal.bleser@opensuse.org
- add mu-* symbolic links
- add Provides for maildir-utils, as that is the name of the mu package on
  Debian
* Sun Feb 13 2011 pascal.bleser@opensuse.org
- initial version (0.9.3)
