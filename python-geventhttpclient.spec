#
# Conditional build:
%bcond_with	tests	# py.test tests [use network]
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	geventhttpclient
Summary:	A high performance, concurrent HTTP client library
Summary(pl.UTF-8):	Biblioteka bardzo wydajnego, wielowątkowego klienta HTTP
Name:		python-%{module}
Version:	1.3.1
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/geventhttpclient
Source0:	https://files.pythonhosted.org/packages/source/g/geventhttpclient/geventhttpclient-%{version}.tar.gz
# Source0-md5:	9aaac96fa4856ac919869a261c8b3dcb
URL:		https://pypi.python.org/pypi/geventhttpclient
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
# older versions generate pythonegg(backports.ssl_match_hostname) dependency
BuildRequires:	python-devel >= 1:2.7.9
BuildRequires:	python-modules >= 1:2.7.9
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-certifi
BuildRequires:	python-gevent >= 0.13
BuildRequires:	python-pytest
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-certifi
BuildRequires:	python3-gevent >= 0.13
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
%endif
Requires:	python-modules >= 1:2.7.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A high performance, concurrent HTTP client library for Python 2 using
gevent.

geventhttpclient use a fast HTTP parser, written in C, originating
from nginx, extracted and modified by Joyent.

geventhttpclient has been specifically designed for high concurrency,
streaming and support HTTP 1.1 persistent connections. More generally
it is designed for efficiently pulling from REST APIs and streaming
API's like Twitter's.

Safe SSL support is provided by default.

%description -l pl.UTF-8
Biblioteka bardzo wydajnego, wielowątkowego klienta HTTP dla Pythona
2, wykorzystująca gevent.

geventhttpclient wykorzystuje szybki parser HTTP, napisany w C,
pochodzący z serwera nginx, wyciągniety i zmodyfikowany przez Joyenta.

geventhttpclient został zaprojektowany w szczególności z myślą o
dużym zrównolegleniu, przesyłaniu strumieni i obsłudze trwałych
połączeń HTTP 1.1. Bardziej ogólnie, jest przeznaczony do wydajnego
pobierania z API REST-owych oraz strumieniowych, takich jak Twitter.

Domyślnie dostępna jest obsługa bezpiecznego SSL.

%package -n python3-%{module}
Summary:	A high performance, concurrent HTTP client library
Summary(pl.UTF-8):	Biblioteka bardzo wydajnego, wielowątkowego klienta HTTP
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
A high performance, concurrent HTTP client library for Python 3 using
gevent.

geventhttpclient use a fast HTTP parser, written in C, originating
from nginx, extracted and modified by Joyent.

geventhttpclient has been specifically designed for high concurrency,
streaming and support HTTP 1.1 persistent connections. More generally
it is designed for efficiently pulling from REST APIs and streaming
API's like Twitter's.

Safe SSL support is provided by default.

%description -n python3-%{module} -l pl.UTF-8
Biblioteka bardzo wydajnego, wielowątkowego klienta HTTP dla Pythona
3, wykorzystująca gevent.

geventhttpclient wykorzystuje szybki parser HTTP, napisany w C,
pochodzący z serwera nginx, wyciągniety i zmodyfikowany przez Joyenta.

geventhttpclient został zaprojektowany w szczególności z myślą o
dużym zrównolegleniu, przesyłaniu strumieni i obsłudze trwałych
połączeń HTTP 1.1. Bardziej ogólnie, jest przeznaczony do wydajnego
pobierania z API REST-owych oraz strumieniowych, takich jak Twitter.

Domyślnie dostępna jest obsługa bezpiecznego SSL.

%prep
%setup -q -n %{module}-%{version}

%{__rm} -r src/geventhttpclient/tests/__pycache__ \
	src/geventhttpclient.egg-info

%build
%if %{with python2}
%py_build

%{?with_tests:PYTHONPATH=$(pwd)/$(echo build-2/lib.*) %{__python} -m pytest src}
%endif

%if %{with python3}
%py3_build

%{?with_tests:PYTHONPATH=$(pwd)/$(echo build-3/lib.*) %{__python3} -m pytest src}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/geventhttpclient/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/geventhttpclient/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%dir %{py_sitedir}/geventhttpclient
%{py_sitedir}/geventhttpclient/*.py[co]
%attr(755,root,root) %{py_sitedir}/geventhttpclient/_parser.so
%{py_sitedir}/geventhttpclient-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%dir %{py3_sitedir}/geventhttpclient
%{py3_sitedir}/geventhttpclient/*.py
%{py3_sitedir}/geventhttpclient/__pycache__
%attr(755,root,root) %{py3_sitedir}/geventhttpclient/_parser.cpython-*.so
%{py3_sitedir}/geventhttpclient-%{version}-py*.egg-info
%endif
