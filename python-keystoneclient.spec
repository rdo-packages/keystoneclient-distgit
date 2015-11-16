%if 0%{?rhel} && 0%{?rhel} <= 6
%global __python2 %{_bindir}/python2
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_version %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")
%endif

%if 0%{?fedora}
%global with_python3 1
%global _docdir_fmt %{name}
%endif

%if 0%{?fedora} || 0%{?rhel} >= 7
%global _bashcompdir %{_datadir}/bash-completion/completions
%else
%global _bashcompdir %{_sysconfdir}/bash_completion.d
%endif

Name:       python-keystoneclient
# Since folsom-2 OpenStack clients follow their own release plan
# and restarted version numbering from 0.1.1
# https://lists.launchpad.net/openstack/msg14248.html
Epoch:      1
Version:    1.7.2
Release:    1%{?dist}
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        https://pypi.python.org/pypi/%{name}
Source0:    https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
%endif

# from requirements.txt
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires: python-argparse
%endif
Requires: python-babel
Requires: python-iso8601 >= 0.1.9
Requires: python-netaddr
Requires: python-oslo-config >= 2:2.3.0
Requires: python-oslo-i18n >= 1.5.0
Requires: python-oslo-serialization >= 1.4.0
Requires: python-oslo-utils >= 2.0.0
Requires: python-prettytable
Requires: python-requests >= 2.5.2
Requires: python-six >= 1.9.0
Requires: python-stevedore >= 1.5.0
Requires: python-pbr
Requires: python-debtcollector >= 0.3.0

# other requirements
Requires: python-setuptools
Requires: python-keyring
# for s3_token middleware
Requires: python-webob

Provides: python2-keystoneclient = %{epoch}:%{version}-%{release}


%description
Client library and command line utility for interacting with Openstack
Identity API.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:    Client library for OpenStack Identity API
# from requirements.txt
Requires: python3-babel
Requires: python3-iso8601 >= 0.1.9
Requires: python3-netaddr
Requires: python3-oslo-config >= 2:2.3.0
Requires: python3-oslo-i18n >= 1.5.0
Requires: python3-oslo-serialization >= 1.4.0
Requires: python3-oslo-utils >= 2.0.0
Requires: python3-prettytable
Requires: python3-requests >= 2.5.2
Requires: python3-six >= 1.9.0
Requires: python3-stevedore >= 1.5.0
Requires: python3-pbr
Requires: python3-debtcollector >= 0.3.0

# other requirements
Requires: python3-setuptools
Requires: python3-keyring
# for s3_token middleware
Requires: python3-webob

%description -n python3-%{srcname}
Client library for interacting with Openstack Identity API.
%endif # with_python3

%package doc
Summary:    Documentation for OpenStack Identity API Client
Group:      Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0

%description doc
Documentation for the client library for interacting with Openstack
Identity API.

%prep
%setup -q

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%install
# install with python2 and rename keystone to keystone-2.x
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/keystone %{buildroot}%{_bindir}/keystone-%{python2_version}

# install with python3 and rename keystone to keystone-3.x
%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/keystone %{buildroot}%{_bindir}/keystone-%{python3_version}
%endif

# setup keystone symlink
%if 0%{?with_python3}
ln -s %{_bindir}/keystone-%{python3_version} %{buildroot}%{_bindir}/keystone
%else
ln -s %{_bindir}/keystone-%{python2_version} %{buildroot}%{_bindir}/keystone
%endif

# bash completion
install -p -D -m 644 tools/keystone.bash_completion %{buildroot}%{_bashcompdir}/keystone

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/tests
%if 0%{?with_python3}
rm -fr %{buildroot}%{python3_sitelib}/tests
%endif

# Build HTML docs and man page
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man
install -p -D -m 644 man/keystone.1 %{buildroot}%{_mandir}/man1/keystone.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{_bindir}/keystone-%{python2_version}
%if ! 0%{?with_python3}
%{_bindir}/keystone
%endif
%{_bashcompdir}/keystone
%{python2_sitelib}/*
%{_mandir}/man1/keystone.1*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{_bindir}/keystone-%{python3_version}
%{_bindir}/keystone
%{_bashcompdir}/keystone
%{python3_sitelib}/*
%{_mandir}/man1/keystone.1*
%endif # with_python3

%files doc
%doc html

%changelog
* Tue Oct 06 2015 Alan Pevec <alan.pevec@redhat.com> 1:1.7.2-1
- Update to upstream 1.7.2

* Fri Sep 11 2015 Alan Pevec <alan.pevec@redhat.com> 1:1.7.1-1
- Update to upstream 1.7.1

* Sun Sep 06 2015 Alan Pevec <alan.pevec@redhat.com> 1:1.7.0-1
- Update to upstream 1.7.0

* Fri Jul 24 2015 Parag Nemade <pnemade@redhat.com> 1:1.6.0-1
- Update to upstream 1.6.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Mar 28 2015 Alan Pevec <alan.pevec@redhat.com> 1:1.3.0-1
- Update to upstream 1.3.0

* Mon Nov 10 2014 Alan Pevec <alan.pevec@redhat.com> 1:0.11.2-1
- Update to upstream 0.11.2

* Tue Sep 30 2014 Alan Pevec <alan.pevec@redhat.com> 1:0.11.1-1
- Update to upstream 0.11.1

* Thu Aug 14 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:0.10.1-1
- Update to upstream 0.10.1
- New Requires: python-stevedore, python-lxml

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 05 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:0.9.0-1
- Update to upstream 0.9.0

* Tue Apr 22 2014 Pádraig Brady <pbrady@redhat.com> - 1:0.8.0-2
- Depend on newer python-six

* Thu Apr 17 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:0.8.0-1
- Update to upstream 0.8.0

* Tue Apr 01 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:0.7.1-1
- Update to upstream 0.7.1

* Fri Feb 21 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.6.0-1
- Update to upstream 0.6.0

* Mon Jan 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.4.2-1
- Update to upstream 0.4.2
- Align doc build with other client packages

* Fri Jan 03 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.4.1-4
- Don't require an email address when creating a user

* Mon Oct 28 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.4.1-3
- Remove unused requires: d2to1, simplejson

* Mon Oct 21 2013 Alan Pevec <apevec@redhat.com> 0.4.1-2
- webob is no longer used in authtoken

* Fri Oct 18 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.4.1-1
- Update to upstream 0.4.1

* Thu Sep 19 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-6
- Include upstream man page.

* Wed Sep 18 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-5
- Remove bogus python-httplib2 dependency.

* Mon Sep 16 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-4
- Add python-netaddr dependency.

* Tue Sep 10 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-3
- Add python-httplib2 dependency.

* Mon Sep 09 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-2
- Remove pbr deps in the patch instead of this spec file.

* Mon Sep 09 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-1
- Update to upstream 0.3.2.
- Ec2Signer patch is included in this version.

* Mon Aug 05 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.1-4
- Ec2Signer: Allow signature verification for older boto versions. (#984752)

* Fri Aug 02 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.1-3
- Remove requirements files.

* Mon Jul 08 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.1-1
- Update to upstream version 0.3.1.

* Tue Jun 25 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.5-2
- Remove runtime dependency on python-pbr.

* Tue Jun 25 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.5-1
- Update to latest upstream. (0.2.5 + patches)
- Add new python requires from requirements.txt. (d2to1, pbr, six)

* Tue May 28 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-4
- Check token expiry. (CVE-2013-2104)

* Thu May 02 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-3
- Config value for revocation list timeout. (#923519)

* Thu Apr 04 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-2
- Update requires. (#948244)

* Tue Mar 19 2013 Alan Pevec <apevec@redhat.com> 0.2.3-1
- New upstream release.

* Wed Jan 30 2013 Alan Pevec <apevec@redhat.com> 0.2.2-1
- New upstream release.

* Thu Jan 17 2013 Alan Pevec <apevec@redhat.com> 0.2.1-2
- Add dependency on python-requests.
- Add python-keyring RPM dependency.

* Fri Dec 21 2012 Alan Pevec <apevec@redhat.com> 0.2.1-1
- New upstream release.
- Add bash completion support

* Fri Nov 23 2012 Alan Pevec <apevec@redhat.com> 0.2.0-1
- New upstream release.
- Identity API v3 support
- add service_id column to endpoint-list
- avoid ValueError exception for 400 or 404 lp#1067512
- use system default CA certificates lp#106483
- keep original IP lp#1046837
- avoid exception for an expected empty catalog lp#1070493
- fix keystoneclient against Rackspace Cloud Files lp#1074784
- blueprint solidify-python-api
- blueprint authtoken-to-keystoneclient-repo
- fix auth_ref initialization lp#1078589
- warn about bypassing auth on CLI lp#1076225
- check creds before token/endpoint lp#1076233
- check for auth URL before password lp#1076235
- fix scoped auth for non-admins lp#1081192

* Tue Oct 16 2012 Alan Pevec <apevec@redhat.com> 0.1.3.27-1
- Allow empty description for tenants (lp#1025929)
- Documentation updates
- change default  wrap for tokens from 78 characters to 0 (lp#1061514)
- bootstrap a keystone user in one cmd
- Useful message when missing catalog (lp#949904)

* Thu Sep 27 2012 Alan Pevec <apevec@redhat.com> 1:0.1.3.9-1
- Handle "503 Service Unavailable" exception (lp#1028799)
- add --wrap option for long PKI tokens (lp#1053728)
- remove deprecated Diablo options
- add --os-token and --os-endpoint options to match
  http://wiki.openstack.org/UnifiedCLI/Authentication

* Sun Sep 23 2012 Alan Pevec <apevec@redhat.com> 1:0.1.3-1
- Change underscores in new cert options to dashes (lp#1040162)

* Wed Aug 22 2012 Alan Pevec <apevec@redhat.com> 1:0.1.2-1
- Add dependency on python-setuptools (#850842)
- New upstream release.

* Mon Jul 23 2012 Alan Pevec <apevec@redhat.com> 1:0.1.1-1
- New upstream release.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2-0.2.f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-1
- Essex release

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.8.rc2
- essex rc2

* Sat Mar 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.7.rc1
- update to final essex rc1

* Wed Mar 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.6.rc1
- essex rc1

* Thu Mar 01 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.5.e4
- essex-4 milestone

* Tue Feb 28 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.4.e4
- Endpoints: Add create, delete, list support
  https://review.openstack.org/4594

* Fri Feb 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.3.e4
- Improve usability of CLI. https://review.openstack.org/4375

* Mon Feb 20 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.2.e4
- pre essex-4 snapshot, for keystone rebase

* Thu Jan 26 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.e3
- Initial package
