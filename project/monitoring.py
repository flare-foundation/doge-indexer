import os
import re

import pkg_resources
from django.conf import settings
from pip_requirements_parser import RequirementsFile
from rest_framework import mixins, serializers, viewsets


def get_requirements(file):
    requirements_file = RequirementsFile.from_file(file)

    options = requirements_file.options
    requirements = requirements_file.requirements
    for option in options:
        for req_file in option.to_dict().get("requirements", []):
            file_name = os.path.dirname(file) + "/" + req_file
            if os.path.exists(file_name):
                requirements.extend(get_requirements(file_name))

    return requirements


class RequirementData:
    def __init__(self, name, installed_version, required_version):
        self.name = name
        self.version = installed_version

        if required_version is not None:
            self.requirement = []
            if required_version:
                for condition in required_version.split(","):
                    r = re.search("(?P<operator>[<>=]+)(?P<version>.+)", condition)
                    self.requirement.append((r.group("operator"), r.group("version")))
        else:
            self.requirement = None


def get_packages_info():
    if hasattr(get_packages_info, "__result"):
        return get_packages_info.__result

    requirements = {req_line.name: req_line.specifier for req_line in get_requirements(settings.REQUIREMENTS_FILE)}
    resources = {resource.project_name: resource.version for resource in pkg_resources.working_set}

    package_list = []
    for name, version in resources.items():
        required = None
        if name in requirements:
            if requirements[name] is None:
                required = ""
            else:
                required = str(requirements[name])
        package_list.append(RequirementData(name, version, required))

    get_packages_info.__result = tuple(package_list)

    return get_packages_info.__result


class RequirementSerializer(serializers.Serializer):
    name = serializers.CharField()
    version = serializers.CharField()
    requirement = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2),
        allow_null=True,
    )


class RequirementsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = get_packages_info()
    serializer_class = RequirementSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
