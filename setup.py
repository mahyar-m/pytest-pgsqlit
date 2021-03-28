#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-ipgsql',
    version='0.1.1',
    author='Mahyar Mostowfi',
    author_email='mahyar.mostowfi@gmail.com',
    maintainer='Mahyar Mostowfi',
    maintainer_email='mahyar.mostowfi@gmail.com',
    license='MIT',
    url='https://github.com/mahyar-m/pytest-ipgsql',
    description='A simple plugin to use with pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_ipgsql'],
    python_requires='>=3.5',
    install_requires=[
        'pytest>=3.5.0',
        'psycopg2-binary'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'pytest11': [
            'pytest_ipgsql = pytest_ipgsql.plugin',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)