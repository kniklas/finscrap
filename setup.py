"Package definition file"

import re
from os.path import basename
from os.path import splitext
from glob import glob

import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Obtain version from __init__.py
with open("src/finscrap/__init__.py", "r", encoding="utf-8") as module_file:
    metadata = dict(
        re.findall(
            r"__([a-zA-Z]+)__\s*=\s*['\"]([^'\"]*)['\"]", module_file.read()
        )
    )

NAME = "finscrap"
version = metadata["version"]
min_python_version = metadata["minPythonVer"]

setuptools.setup(
    name=NAME,
    author="Kamil Niklasinski",
    license="MIT License",
    author_email="kamil.niklasinski@gmail.com",
    version=version,
    keywords="NBP API FX",
    description="Get FX is tool to retrieve average FX rates from NBP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=["requests"],
    setup_requires=["setuptools", "wheel"],
    entry_points={"console_scripts": ["getfx = getfx.getfxnbp:init_cmd"]},
    project_urls={
        "Issue tracker": "https://github.com/kniklas/get-fx/issues",
        "Documentation": "https://kniklas.github.io/get-fx/",
        "Source": "https://github.com/kniklas/get-fx",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=" + min_python_version,
    platforms="any",
)
