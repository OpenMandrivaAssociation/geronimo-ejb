%global spec_ver 3.1
%global spec_name geronimo-ejb_%{spec_ver}_spec

Name:             geronimo-ejb
Version:          1.0
Release:          6
Summary:          Java EE: EJB API v3.1
Group:            Development/Java
License:          ASL 2.0
URL:              http://geronimo.apache.org

Source0:          http://repo2.maven.org/maven2/org/apache/geronimo/specs/%{spec_name}/%{version}/%{spec_name}-%{version}-source-release.tar.gz
# Use parent pom files instead of unavailable 'genesis-java5-flava'
Patch1:           use_parent_pom.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    maven2 >= 2.2.1
BuildRequires:    geronimo-parent-poms
BuildRequires:    maven-resources-plugin
BuildRequires:    jta
BuildRequires:    interceptor_api
BuildRequires:    annotation_api
BuildRequires:    jaxrpc_api
BuildRequires:    geronimo-osgi-locator

Requires:         jta
Requires:         interceptor_api
Requires:         annotation_api
Requires:         jaxrpc_api
Requires:         geronimo-osgi-locator
Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

Provides:         ejb_api = %{spec_ver}

%description
Contains the Enterprise JavaBeans classes and interfaces that define the 
contracts between the enterprise bean and its clients and between the 
enterprise bean and the EJB container. 

%package javadoc
Group:            Development/Java
Summary:          Javadoc for %{name}
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{spec_name}-%{version}
sed -i 's/\r//' LICENSE
%patch1 -p0

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{spec_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/ejb.jar

# poms
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.apache.geronimo.specs %{spec_name} %{version} JPP %{name}
%add_to_maven_depmap org.apache.geronimo.specs geronimo-ejb_2.1_spec 1.1 JPP %{name}
%add_to_maven_depmap org.apache.geronimo.specs geronimo-ejb_3.0_spec 1.0.1 JPP %{name}
%add_to_maven_depmap javax.ejb ejb %{spec_ver} JPP %{name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

