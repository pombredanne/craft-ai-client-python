#!/usr/bin/env python
from codecs import open
from os import path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name='craft-ai',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    # version='0.1',

    description='craft ai API client for python',
    long_description=readme(),

    author='craft.ai team',
    author_email='contact@craft.ai',
    url='https://github.com/craft-ai/craft-ai-client-python/',

    # Choose your license
    license='BSD 3-Clause',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Python versions against which the code has been tested and is
        # actively supported.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='ai craft-ai',

    packages=['craftai'],
    install_requires=['requests', 'six'],
    extras_require={
        'dev': ['python-dotenv'],
        'test': ['tox', 'nose']
    },

    include_package_data=True,
    entry_points={
        'console_scripts': [
            'update_readme= cli:update_readme'
        ]
    }
)
