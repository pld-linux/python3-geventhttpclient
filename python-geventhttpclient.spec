#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	geventhttpclient
Summary:	A high performance, concurrent HTTP client library
Name:		python-%{module}
Version:	1.2.0
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/g/geventhttpclient/geventhttpclient-%{version}.tar.gz
# Source0-md5:	1b3070e09b6e50fce929771f3f4fc9a6
URL:		https://pypi.python.org/pypi/geventhttpclient
BuildRequires:	python-gevent
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-certifi
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-certifi
%endif
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A high performance, concurrent HTTP client library for Python using
gevent.

geventhttpclient use a fast HTTP parser, written in C, originating
from nginx, extracted and modified by Joyent.

geventhttpclient has been specifically designed for high concurrency,
streaming and support HTTP 1.1 persistent connections. More generally
it is designed for efficiently pulling from REST APIs and streaming
API's like Twitter's.

Safe SSL support is provided by default.

%package -n python3-%{module}
Summary:	A high performance, concurrent HTTP client library
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
A high performance, concurrent HTTP client library for Python using
gevent.

geventhttpclient use a fast HTTP parser, written in C, originating
from nginx, extracted and modified by Joyent.

geventhttpclient has been specifically designed for high concurrency,
streaming and support HTTP 1.1 persistent connections. More generally
it is designed for efficiently pulling from REST APIs and streaming
API's like Twitter's.

Safe SSL support is provided by default.

%prep
%setup -q -n %{module}-%{version}

# setup copy of source in py3 dir
set -- *
install -d py3
cp -a "$@" py3

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%dir %{py_sitedir}/geventhttpclient
%{py_sitedir}/geventhttpclient/*.py[co]
%attr(755,root,root) %{py_sitedir}/geventhttpclient/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE
%{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif
