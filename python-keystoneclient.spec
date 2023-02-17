%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Client library and command line utility for interacting with Openstack \
Identity API.

%global sname keystoneclient
%global with_doc 1

Name:       python-keystoneclient
Epoch:      1
Version:    XXX
Release:    XXX
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        https://launchpad.net/python-keystoneclient
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires: /usr/bin/openssl


%description
%{common_desc}

%package -n python3-%{sname}
Summary:    Client library for OpenStack Identity API
%{?python_provide:%python_provide python3-%{sname}}
Obsoletes: python2-%{sname} < %{version}-%{release}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr >= 2.0.0
BuildRequires: git-core

Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-requests >= 2.14.2
Requires: python3-six >= 1.10.0
Requires: python3-stevedore >= 1.20.0
Requires: python3-pbr >= 2.0.0
Requires: python3-debtcollector >= 1.2.0
Requires: python3-keystoneauth1 >= 3.4.0
Requires: python3-keyring >= 5.5.1
Requires: python3-packaging >= 20.4

%description -n python3-%{sname}
%{common_desc}

%package -n python3-%{sname}-tests
Summary:  Python API and CLI for OpenStack Keystone (tests)
%{?python_provide:%python_provide python3-%{sname}-tests}
Requires:  python3-%{sname} = %{epoch}:%{version}-%{release}

BuildRequires:  python3-hacking
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-oauthlib
BuildRequires:  python3-oslotest
BuildRequires:  python3-testtools
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-stestr
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-requests-mock
BuildRequires:  python3-keyring >= 5.5.1
BuildRequires:  python3-lxml

Requires:  python3-hacking
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-oauthlib
Requires:  python3-oslotest
Requires:  python3-stestr
Requires:  python3-testtools
Requires:  python3-testresources
Requires:  python3-testscenarios
Requires:  python3-requests-mock
Requires:  python3-lxml

%description -n python3-%{sname}-tests
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: Documentation for OpenStack Keystone API client

BuildRequires: python3-sphinx
BuildRequires: python3-sphinxcontrib-apidoc
BuildRequires: python3-openstackdocstheme

%description -n python-%{sname}-doc
%{common_desc}
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

# disable warning-is-error, this project has intersphinx in docs
# so some warnings are generated in network isolated build environment
# as koji
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%{py3_build}

%install
%{py3_install}

%if 0%{?with_doc}
# Build HTML docs
# Disable warning-is-error as intersphinx extension tries
# to access external network and fails.
sphinx-build -b html doc/source doc/build/html
# Drop intersphinx downloaded file objects.inv to avoid rpmlint warning
rm -fr doc/build/html/objects.inv
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif

%check
# TODO(amoralej) disabling cms tests https://bugs.launchpad.net/python-keystoneclient/+bug/1963925
PYTHON=%{__python3} stestr --test-path=./keystoneclient/tests/unit run --exclude-regex '^.*test_cms.*'

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{sname}/tests

%changelog
