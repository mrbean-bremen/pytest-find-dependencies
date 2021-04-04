#!/usr/bin/env python
import codecs
import os

from setuptools import setup, find_packages
from src.find_dependencies import __version__


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-find-dependencies',
    version=__version__,
    author='MrBean Bremen',
    author_email='hansemrbean@googlemail.com',
    maintainer='MrBean Bremen',
    maintainer_email='hansemrbean@googlemail.com',
    license='MIT',
    url='https://github.com/mrbean-bremen/pytest-find-dependencies',
    description='A pytest plugin to find dependencies between tests',
    long_description=read('README.rst'),
    py_modules=['pytest_find_dependencies'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "pytest11": ["find_dependencies = find_dependencies.plugin"]
    }
)
