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
    keywords="webscraping funds shareclass",
    description="Tool to webscrap financial data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=["requests", "bs4"],
    setup_requires=["setuptools", "wheel"],
    project_urls={
        "Issue tracker": "https://github.com/kniklas/finscrap/issues",
        "Source": "https://github.com/kniklas/finscrap",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=" + min_python_version,
    platforms="any",
)
