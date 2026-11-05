%global spec_ver 3.1
%global spec_name geronimo-ejb_%{spec_ver}_spec
%bcond_with javadoc

Name:             geronimo-ejb
Version:          1.0.2
Release:          1
Summary:          Java EE: EJB API v3.1

License:          ASL 2.0
URL:              https://geronimo.apache.org

Source0:          https://repo1.maven.org/maven2/org/apache/geronimo/specs/%{spec_name}/%{version}/%{spec_name}-%{version}-source-release.tar.gz

BuildArch:        noarch
BuildRequires:    python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name} --link ejb --alias org.apache.geronimo.specs:geronimo-ejb_2.1_spec --alias org.apache.geronimo.specs:geronimo-ejb_3.0_spec --alias javax.ejb:ejb --alias javax.ejb:ejb-api

BuildRequires:    geronimo-jta

Provides:         ejb_api = %{spec_ver}

%description
Contains the Enterprise JavaBeans classes and interfaces that define the
contracts between the enterprise bean and its clients and between the
enterprise bean and the EJB container.

%if %{with javadoc}
%package javadoc
Summary:          Javadoc for %{name}

%endif
%if %{with javadoc}
%description javadoc
This package contains the API documentation for %{name}.


%endif
%prep
%setup -q -n %{spec_name}-%{version}
sed -i 's/\r//' LICENSE
# genesis-java5-flava is not packaged. Coordinates are already on this POM.
# The parent registered bundle packaging. Load the bundle plugin as an extension.
python - <<'PY'
import re
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
text = re.sub(r"\s*<parent>.*?</parent>", "", text, count=1, flags=re.S)
text = re.sub(
    r"(<artifactId>maven-bundle-plugin</artifactId>)",
    r"\1\n                <extensions>true</extensions>",
    text,
    count=1,
)
path.write_text(text)
PY



%files -f .mfiles
%doc LICENSE NOTICE

%if %{with javadoc}
%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%endif
