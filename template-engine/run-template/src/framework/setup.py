#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

readme = "readme_file.read()"

history = "history_file.read()"

requirements = [
    'questionary',
    'pyyaml',
    'hiyapyco',
    'Jinja2<3,>1',
    'jsonmerge>=1.8.0',
    'jinja2-strcase',
    'unidecode>=1.2.0']

test_requirements = []

setup(
    author="zup",
    author_email='zup@zup.com.br',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    description="a framework to create templates",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    keywords='templateframework',
    name='templateframework',
    packages=find_packages(include=['templateframework', 'templateframework.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Orangestack-com/stacklifecycle-scaffold-engine-org',
    version='0.1.0',
    zip_safe=False,
)
