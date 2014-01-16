%{?_javapackages_macros:%_javapackages_macros}
%global spec_ver 3.1
%global spec_name geronimo-ejb_%{spec_ver}_spec

Name:             geronimo-ejb
Version:          1.0
Release:          12.0%{?dist}
Summary:          Java EE: EJB API v3.1

License:          ASL 2.0
URL:              http://geronimo.apache.org

Source0:          http://repo2.maven.org/maven2/org/apache/geronimo/specs/%{spec_name}/%{version}/%{spec_name}-%{version}-source-release.tar.gz

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    geronimo-parent-poms
BuildRequires:    jta
BuildRequires:    interceptor_api
BuildRequires:    annotation_api
BuildRequires:    jaxrpc_api
BuildRequires:    geronimo-osgi-locator

Provides:         ejb_api = %{spec_ver}

%description
Contains the Enterprise JavaBeans classes and interfaces that define the
contracts between the enterprise bean and its clients and between the
enterprise bean and the EJB container.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{spec_name}-%{version}
sed -i 's/\r//' LICENSE
# Use parent pom files instead of unavailable 'genesis-java5-flava'
%pom_set_parent org.apache.geronimo.specs:specs:1.4

%mvn_alias : org.apache.geronimo.specs:geronimo-ejb_2.1_spec
%mvn_alias : org.apache.geronimo.specs:geronimo-ejb_3.0_spec
%mvn_alias : javax.ejb:ejb
%mvn_alias : javax.ejb:ejb-api

%mvn_file : %{name} ejb

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Thu Aug 15 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0-12
- Add dependency mapping for javax.ejb:ejb-api, rhbz #826859

* Thu Aug  8 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-11
- Update to latest packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0-9
- Change BR from maven2 to maven-local, fixes FTBFS rhbz #914027

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-5
- Build with maven 3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 5 2010 Chris Spike <chris.spike@arcor.de> 1.0-3
- Fixed missing BR maven2
- Fixed missing BR geronimo-parent-poms
- Fixed missing BR maven-resources-plugin

* Wed Aug 4 2010 Chris Spike <chris.spike@arcor.de> 1.0-2
- Fixed wrong EOL encoding in LICENSE
- Removed custom depmap
- Added 'org.apache.geronimo.specs:geronimo-ejb_2.1_spec' to maven depmap
- Added 'org.apache.geronimo.specs:geronimo-ejb_3.0_spec' to maven depmap

* Thu Jul 22 2010 Chris Spike <chris.spike@arcor.de> 1.0-1
- Initial version of the package
