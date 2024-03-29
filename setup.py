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
    version='1.2.0',  # Don't forget to update the changelog and __init__.py!
    description='A simple lexer based on regular expressions',
    long_description=long_description,
    url='https://github.com/Parquery/lexery',
    author='Marko Ristin',
    author_email='marko@ristin.ch',
    # yapf: disable
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    # yapf: enable
    keywords='lexer regexp regular expression',
    license='License :: OSI Approved :: MIT License',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[],
    extras_require={
        'dev': ['mypy==1.2.0', 'pylint==2.17.2', 'yapf==0.20.2', 'coverage>=4.5.1,<5', 'pydocstyle==6.1.1']
    },
    py_modules=['lexery'],
    package_data={"lexery": ["py.typed"]})
