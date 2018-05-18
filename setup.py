#!/usr/bin/env python

from setuptools import setup, find_packages
# import numpy as np
# from Cython.Build import cythonize

install_requires = [
    'pysam>=0.14.0',
    'tqdm>=4.23.0',
    'numpy>=1.14.0',
    'pandas>=0.22.0',
    'mypy-protobuf>=1.3',
    "grpcio-tools>=1.11",
]

setup(
    name="minion_data",
    version='0.2.0',
    description='',
    url='https://github.com/nmiculinic/minion-data',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    author='Neven Miculinic',
    author_email='neven.miculinic@gmail.com',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',

    ],

    project_urls={  # Optional
        'Source': 'https://github.com/nmiculinic/minion-data/',
    },

)
