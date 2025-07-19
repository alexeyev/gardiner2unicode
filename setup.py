# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="gardiner2unicode",
    packages=find_packages(),
    version="0.0.3",
    description="Mapping Gardiner's codes to Unicode + generating corresponding images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anton Alekseev",
    author_email="anton.m.alexeye@gmail.com",
    url="https://github.com/alexeyev/gardiner2unicode",
    keywords=["egyptology", "ancient egypt", "fonts"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    package_data={
        "gardiner2unicode": ["data/*.wiki"],
    },
    include_package_data=True,
)
