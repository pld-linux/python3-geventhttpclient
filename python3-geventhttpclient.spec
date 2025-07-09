#
# Conditional build:
%bcond_with	tests	# py.test tests [use network, missing tests.common file in sdist]

%define 	module	geventhttpclient
Summary:	A high performance, concurrent HTTP client library
Summary(pl.UTF-8):	Biblioteka bardzo wydajnego, wielowątkowego klienta HTTP
Name:		python3-%{module}
Version:	2.3.4
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/geventhttpclient/
Source0:	https://files.pythonhosted.org/packages/source/g/geventhttpclient/geventhttpclient-%{version}.tar.gz
# Source0-md5:	34d06a7fadb54de4aeac889c44643a29
URL:		https://pypi.org/project/geventhttpclient/
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-brotli
BuildRequires:	python3-certifi
BuildRequires:	python3-dpkt
BuildRequires:	python3-gevent >= 0.13
BuildRequires:	python3-pytest
BuildRequires:	python3-requests
BuildRequires:	python3-urllib3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.9
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

%prep
%setup -q -n %{module}-%{version}

%{__rm} -r src/geventhttpclient.egg-info

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/$(echo build-3/lib.*) \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{py3_sitedir}/geventhttpclient
%{py3_sitedir}/geventhttpclient/*.py
%{py3_sitedir}/geventhttpclient/__pycache__
%attr(755,root,root) %{py3_sitedir}/geventhttpclient/_parser.cpython-*.so
%{py3_sitedir}/geventhttpclient-%{version}-py*.egg-info
