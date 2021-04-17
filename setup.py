#!/usr/bin/env python

"""The setup script."""

from os import path
from setuptools import setup, find_packages

CURRENT_PATH = path.abspath(path.dirname(__file__))

with open(path.join(CURRENT_PATH, "README.md")) as file:
    readme = file.read()

with open(path.join(CURRENT_PATH, "HISTORY.md")) as file:
    history = file.read()

requirements = ['numpy', 'matplotlib', 'scipy']

setup_requirements = [
    'pytest-runner',
]

test_requirements = ["flake8", "coverage", "pytest>=3", "pytest-runner>=5"]

doc_requirements = ["Sphinx>1.8"]

dev_requirements = ["bump2version", "twine"]

setup(
    author="Ondrej Lexa",
    author_email='lexa.ondrej@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Python module for heat transfer modelling for students",
    install_requires=requirements,
    extras_require={
        "tests": test_requirements,
        "docs": doc_requirements,
        "dev": dev_requirements + test_requirements + doc_requirements,
    },
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='heatlib',
    name='heatlib',
    packages=find_packages(include=['heatlib', 'heatlib.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ondrolexa/heat/ondrolexa/heatlib',
    version='0.1.0',
    zip_safe=False,
)
