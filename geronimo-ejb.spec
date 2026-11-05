%global spec_ver 3.1
%global spec_name geronimo-ejb_%{spec_ver}_spec
%bcond_with javadoc

Name:             geronimo-ejb
Version:          1.0.2
Release:          1
Summary:          Java EE: EJB API v3.1
Group:            Development/Java
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
BuildRequires:    geronimo-jaxrpc
BuildRequires:    geronimo-osgi-locator

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
# genesis-java5-flava is not packaged. Annotation and interceptor APIs are
# not imported. Bundle packaging needs a plugin we do not ship.
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def local(tag):
    return tag.split("}", 1)[-1]

tree = ET.parse("pom.xml")
root = tree.getroot()
for node in list(root):
    if local(node.tag) in {"parent", "build", "distributionManagement"}:
        root.remove(node)
for node in root.iter(f"{{{NS}}}packaging"):
    node.text = "jar"
drop = {"geronimo-interceptor_1.1_spec", "geronimo-annotation_1.1_spec"}
for deps in list(root):
    if local(deps.tag) != "dependencies":
        continue
    for dep in list(deps):
        artifact = ""
        for node in dep:
            if local(node.tag) == "artifactId":
                artifact = (node.text or "").strip()
        if artifact in drop:
            deps.remove(dep)
tree.write("pom.xml", encoding="utf-8", xml_declaration=True)
PY



%files -f .mfiles
%doc LICENSE NOTICE

%if %{with javadoc}
%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%endif
