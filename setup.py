#!/usr/bin/env python

from setuptools import setup, find_packages
# import numpy as np
# from Cython.Build import cythonize

install_requires=[
]

setup(
    name="minino_data",
    version='0.1',
    description='',
    url='https://github.com/nmiculinic/minion-data',
    packages=['minion_data'],
    include_package_data=True,
    install_requires=install_requires,
    author = 'Neven Miculinic',
    author_email = 'neven.miculinic@gmail.com',
    # ext_modules=cythonize("fino/arbitrage.pyx"),
    # include_dirs=[np.get_include()],
)
