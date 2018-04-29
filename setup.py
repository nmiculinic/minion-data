#!/usr/bin/env python

from setuptools import setup, find_packages
# import numpy as np
# from Cython.Build import cythonize

install_requires=[
    'pysam>=0.14.0',
    'tqdm>=4.23.0',
    'numpy>=1.14.0',
    'pandas>=0.22.0',
    'mypy-protobuf>=1.3',
    "grpcio-tools>=1.11",
]

setup(
    name="minion_data",
    version='0.1',
    description='',
    url='https://github.com/nmiculinic/minion-data',
    packages=['minion_data'],
    include_package_data=True,
    install_requires=install_requires,
    author='Neven Miculinic',
    author_email='neven.miculinic@gmail.com',
    # ext_modules=cythonize("example.pyx"),
    # include_dirs=[np.get_include()],
)
