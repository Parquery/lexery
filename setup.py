"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os

from setuptools import setup, find_packages

# pylint: disable=redefined-builtin
here = os.path.abspath(os.path.dirname(__file__))  # pylint: disable=invalid-name
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()  # pylint: disable=invalid-name

setup(
    name='lexery',
    version='1.1.1',  # Don't forget to update the changelog!
    description='A simple lexer based on regular expressions',
    long_description=long_description,
    url='https://github.com/Parquery/lexery',
    author='Marko Ristin',
    author_email='marko@parquery.com',
    # yapf: disable
    classifiers=[
        'Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    # yapf: enable
    keywords='lexer regexp regular expression',
    license='License :: OSI Approved :: MIT License',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[],
    extras_require={
        'dev': ['mypy==0.790', 'pylint==2.6.0', 'yapf==0.20.2', 'coverage>=4.5.1,<5', 'pydocstyle>=2.1.1,<3']
    },
    py_modules=['lexery'],
    package_data={"lexery": ["py.typed"]})
