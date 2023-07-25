%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

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
License:    Apache-2.0
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

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: git-core
# keyring is a optional dep but we are maintataining as default for backwards
# compatibility
Requires: python3-keyring >= 5.5.1

%description -n python3-%{sname}
%{common_desc}

%package -n python3-%{sname}-tests
Summary:  Python API and CLI for OpenStack Keystone (tests)

Requires:  python3-%{sname} = %{epoch}:%{version}-%{release}
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

%description -n python-%{sname}-doc
%{common_desc}
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_doc}
# Build HTML docs
# Disable warning-is-error as intersphinx extension tries
# to access external network and fails.
%tox -e docs
# Drop intersphinx downloaded file objects.inv to avoid rpmlint warning
rm -fr doc/build/html/objects.inv
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif

%check
%tox -e %{default_toxenv} -- -- --exclude-regex '^.*test_cms.*'

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.dist-info
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
# REMOVEME: error caused by commit https://opendev.org/openstack/python-keystoneclient/commit/4763cd8052f51393063cc8706fdc0f0c9b017b24
