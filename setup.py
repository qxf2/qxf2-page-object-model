from setuptools import setup

with open("Readme.md", "r") as fh:
    _long_description = fh.read()

_classifiers = [
    "Development Status :: 1 - BETA",
]

_console_scripts = [
    "create-repo=qxf2.utils:create_repo",
]

with open("requirements.txt", "r") as reqfile:
    _requirements = reqfile.read().splitlines()

with open("LICENSE", "r") as licensefile:
    _license = licensefile.read()

setup(
    author="shivahariP",
    author_email="shivahari@qxf2.com",
    classifiers=_classifiers,
    description="Qxf2 Services Testing Framework",
    entry_points=dict(console_scripts=_console_scripts),
    license=_license,
    long_description=_long_description,
    name="qxf2",
    packages=["qxf2"],
    url="https://www.qxf2.com",
    version="0.0.1",
    zip_safe=True,
    install_requires=_requirements,
)
