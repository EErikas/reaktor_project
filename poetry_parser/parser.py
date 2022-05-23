import re


class Package:
    def __init__(self, text):
        self.__dependencies = []
        self.__extras = []
        for section in text.split('[package.'):
            if section.startswith('dependencies'):
                for line in section.split('\n')[1:]:
                    self.__dependencies.append({'name': line.split(" =")[0]})
            elif section.startswith('extras'):

                for line in section.split('\n')[1:]:
                    name, dependencies = line.split(' = [')

                    # Remove unwanted chars from dependencies
                    dependencies = dependencies[:-1]
                    dependencies = re.sub('.\((.*?)\)', '', dependencies, flags=re.DOTALL)
                    dependencies = dependencies.replace('"', '')
                    dependencies = dependencies.replace(' ', '')

                    # Add cleaned extra package descriptor:
                    self.__extras.append(
                        {
                            'name': name,
                            'dependencies': [{'name': foo} for foo in dependencies.split(',')]
                        }
                    )
            else:
                self.__name = re.findall(r'name = "(.*?)"', section)[0]
                self.__description = re.findall(r'description = "(.*?)"', section)[0]

    def get_package(self):
        return {
            'name': self.__name,
            'description': self.__description,
            'dependencies': self.__dependencies,
            'extras': self.__extras
        }

    def print_info(self):
        print(f"""---
        Name: {self.__name}
        Description: {self.__description}
        Dependencies: {self.__dependencies}
        Extras: {self.__extras}""")


class PackageParser:
    __supported_versions = ['1.1']

    def __init__(self, text):
        self.__packages = []
        self.__warnings = []

        if text == '':
            self.__warnings.append(
                {
                    'level': 'critical',
                    'description': 'File is empty'
                }
            )
        # Creat list of elements split by metadata tag
        try:
            packages, metadata = text.split('[metadata]')
        except ValueError:
            self.__warnings.append(
                {
                    'level': 'critical',
                    'description': 'Provided file could not be parsed'
                }
            )
            return
        # Extract and check version number
        try:
            self.__version = re.findall(r'version = "(.*?)"', metadata)[0]
            if self.__version not in self.__supported_versions:
                self.__warnings.append(
                    {
                        'level': 'warning',
                        'description': f'Version {self.__version} is not supported. Supported versions are {",".join(self.__supported_versions)}'
                    }
                )
        except IndexError:
            self.__version = ''
            self.__warnings.append(
                {
                    'level': 'critical',
                    'description': 'Version not found'
                }
            )
        # Assemble packages
        for p in packages.split('[[package]]\n')[1:]:
            p = p.replace('\n\n', '')
            foo = Package(p)
            self.__packages.append(foo)

        if len(self.__packages) == 0:
            self.__warnings.append(
                {
                    'level': 'critical',
                    'description': 'No packages found'
                }
            )
        else:
            self.__warnings.append(
                {
                    'level': 'info',
                    'description': f'Packages found: {len(self.__packages)}'
                }
            )

    def no_critical(self):
        for warning in self.__warnings:
            if warning.get('level') == 'critical':
                return False
        return True

    def get_reverse_dependencies(self):
        reverse_deps = {}
        installed_packages = self.get_installed()
        for pkg in installed_packages:
            deps = []
            for foo in self.__packages:
                dependencies = [bar.get('name') for bar in foo.get_package().get('dependencies')]
                pkg_name = foo.get_package().get('name')
                if pkg in dependencies:
                    # If reverse dependency is the base package, "pkg" and "verbose_name" are the same,
                    # e.g., {"pkg" : "pytest", "verbose_name" : "pytest"}
                    deps.append({'pkg': pkg_name, 'verbose_name': pkg_name})
                for extra in foo.get_package().get('extras'):
                    extra_dependencies = [bar.get('name') for bar in extra.get('dependencies')]
                    if pkg in extra_dependencies:
                        # If reverse dependency is in extra, "pkg" is base pkg and "verbose_name" is pkg[extra]
                        # e.g., {"pkg" : "urllib3", "verbose_name" : "urllib3[secure]"}
                        deps.append({'pkg': pkg_name, 'verbose_name': f'{pkg_name}[{extra.get("name")}]'})

            # Add alphabetically sorted reverse dependencies to the list
            reverse_deps.update({pkg: sorted(deps, key=lambda x: x.get('verbose_name'))})
        return reverse_deps

    def get_packages(self):
        installed_packages = self.get_installed()

        for package in self.__packages:
            for dep in package.get_package().get('dependencies'):
                dep.update({'installed': dep.get('name') in installed_packages})
            # Update if extra packages are installed or not
            for extra in package.get_package().get('extras'):
                for dep in extra.get('dependencies'):
                    dep.update({'installed': dep.get('name') in installed_packages})

        return [package.get_package() for package in self.__packages]

    def get_version(self):
        return self.__version

    def get_installed(self):
        return [pkg.get_package().get('name') for pkg in self.__packages]

    def get_warnings(self):
        return self.__warnings
