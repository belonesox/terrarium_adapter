#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]


test_requirements = [ ]

setup(
    author="Stas Fomin",
    author_email='fomin@ispras.ru',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='terrarium_adapter',
    name='terrarium_adapter',
    packages=find_packages(include=['terrarium_adapter', 'terrarium_adapter.*']),
    version_config=True,
    setup_requires=['setuptools-git-versioning'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/belonesox/terrarium_adapter',
    zip_safe=False,
)
