%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif


Name:       python-keystoneclient
Epoch:      1
Version:    3.13.1
Release:    1%{?dist}
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        https://launchpad.net/python-keystoneclient
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: /usr/bin/openssl


%description
Client library and command line utility for interacting with Openstack
Identity API.

%package -n python2-keystoneclient
Summary:    Client library for OpenStack Identity API
%{?python_provide:%python_provide python2-keystoneclient}

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr >= 2.0.0
BuildRequires: git

Requires: python-oslo-config >= 2:4.0.0
Requires: python-oslo-i18n >= 2.1.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-utils >= 3.20.0
Requires: python-requests >= 2.10.0
Requires: python-six >= 1.9.0
Requires: python-stevedore >= 1.20.0
Requires: python-pbr >= 2.0.0
Requires: python-debtcollector >= 1.2.0
Requires: python-positional >= 1.1.1
Requires: python-keystoneauth1 >= 3.1.0
Requires: python-keyring >= 5.5.1

%description -n python2-keystoneclient
Client library and command line utility for interacting with Openstack
Identity API.

%if 0%{?with_python3}
%package -n python3-keystoneclient
Summary:    Client library for OpenStack Identity API
%{?python_provide:%python_provide python3-keystoneclient}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr >= 2.0.0

Requires: python3-oslo-config >= 2:4.0.0
Requires: python3-oslo-i18n >= 2.1.0
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-utils >= 3.20.0
Requires: python3-requests >= 2.10.0
Requires: python3-six >= 1.9.0
Requires: python3-stevedore >= 1.20.0
Requires: python3-pbr >= 2.0.0
Requires: python3-debtcollector >= 1.2.0
Requires: python3-positional >= 1.1.1
Requires: python3-keystoneauth1 >= 3.1.0
Requires: python3-keyring >= 5.5.1

%description -n python3-keystoneclient
Client library for interacting with Openstack Identity API.
%endif

%package -n python2-keystoneclient-tests
Summary:  python2-keystoneclient test subpackage
Requires:  python2-keystoneclient = %{epoch}:%{version}-%{release}

BuildRequires:  python-hacking
BuildRequires:  python-fixtures
BuildRequires:  python-keyring >= 5.5.1
BuildRequires:  python-lxml
BuildRequires:  python-mock
BuildRequires:  python-oauthlib
BuildRequires:  python-oslotest
BuildRequires:  python-requests-mock
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-keystoneauth1
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-i18n

Requires:  python-hacking
Requires:  python-fixtures
Requires:  python-lxml
Requires:  python-mock
Requires:  python-oauthlib
Requires:  python-oslotest
Requires:  python-requests-mock
Requires:  python-testrepository
Requires:  python-testresources
Requires:  python-testscenarios
Requires:  python-testtools


%description -n python2-keystoneclient-tests
python2-keystoneclient test subpackages

%if 0%{?with_python3}
%package -n python3-keystoneclient-tests
Summary:  python3-keystoneclient test subpackage
Requires:  python3-keystoneclient = %{epoch}:%{version}-%{release}

BuildRequires:  python3-hacking
BuildRequires:  python3-fixtures
BuildRequires:  python3-keyring >= 5.5.1
BuildRequires:  python3-lxml
BuildRequires:  python3-mock
BuildRequires:  python3-oauthlib
BuildRequires:  python3-oslotest
BuildRequires:  python3-requests-mock
BuildRequires:  python3-testrepository
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-i18n

Requires:  python3-hacking
Requires:  python3-fixtures
Requires:  python3-lxml
Requires:  python3-mock
Requires:  python3-oauthlib
Requires:  python3-oslotest
Requires:  python3-requests-mock
Requires:  python3-testrepository
Requires:  python3-testresources
Requires:  python3-testscenarios
Requires:  python3-testtools


%description -n python3-keystoneclient-tests
python3-keystoneclient test subpackages
%endif

%package doc
Summary: Documentation for OpenStack Keystone API client

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme

%description doc
Documentation for the keystoneclient module

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# disable warning-is-error, this project has intersphinx in docs
# so some warnings are generated in network isolated build environment
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Build HTML docs
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}


%check
%{__python2} setup.py test
rm -fr .testrepository
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files -n python2-keystoneclient
%license LICENSE
%doc README.rst
%{python2_sitelib}/keystoneclient
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/keystoneclient/tests

%if 0%{?with_python3}
%files -n python3-keystoneclient
%license LICENSE
%doc README.rst
%{python3_sitelib}/keystoneclient
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/keystoneclient/tests
%endif

%files doc
%doc doc/build/html
%license LICENSE

%files -n python2-keystoneclient-tests
%license LICENSE
%{python2_sitelib}/keystoneclient/tests

%if 0%{?with_python3}
%files -n python3-keystoneclient-tests
%license LICENSE
%{python3_sitelib}/keystoneclient/tests
%endif

%changelog
* Wed Apr 24 2019 RDO <dev@lists.rdoproject.org> 1:3.13.1-1
- Update to 3.13.1

* Fri Aug 11 2017 Alfredo Moralejo <amoralej@redhat.com> 1:3.13.0-1
- Update to 3.13.0

