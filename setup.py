"""Setup."""
from setuptools import find_packages, setup

from nanohelp import __version__


def load_long_description(filename: str) -> str:
    """Convert README.md to a string."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="nanohelp",
    version=__version__,
    author="Nathaniel Schultz",
    author_email="nate@nanoswap.finance",
    description="Business logic to abstract the raw nano node RPC logic",
    long_description=load_long_description("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/nanoswap/nanohelp",
    project_urls={
        "Bug Tracker": "https://github.com/nanoswap/nanohelp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)"
    ],
    python_requires=">=3.11",
    package_dir={'nanohelp': "nanohelp"},
    packages=find_packages(exclude=['tests', 'tests.*']),
)
