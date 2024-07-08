"""Setup module for pydrought package in python 3
From:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path
import subprocess


def _get_gdal_version():
    try:
        p = subprocess.Popen(["gdal-config", "--version"], stdout=subprocess.PIPE)
    except FileNotFoundError:
        raise SystemError(
            "gdal-config not found."
            "GDAL seems not installed. "
            "Please, install GDAL binaries and libraries for your system "
            "and then install the relative pip package."
        )
    else:
        return p.communicate()[0].splitlines()[0].decode()


gdal_version = _get_gdal_version()
req_file = "pyproject.toml"
requirements = [l for l in open(req_file).readlines() if l and not l.startswith("#")]
requirements += ["GDAL=={} --no-cache-dir".format(gdal_version)]

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pydrought",
    version="2.1",
    description="Python common modules for EDO, GDO & ICPAC drought data management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="EDO team",
    maintainer_org="ICPAC DRM Team",
    maintainer="Jason Kinyua",
    maintainer_email="jaysnmury@gmail.com",
    packages=find_packages(exclude=["build", "dist", "tests"]),
    package_data={"pydrought": ["*.json", "pydrought/*.json"]},
    include_package_data=True,
    install_requires=requirements,
)
