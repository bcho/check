# coding: utf-8

from setuptools import setup, find_packages

from check import __project__, __version__


README = open('README.md').read()
CHANGES = open('CHANGES.md').read()


setup(
    name=__project__,
    version=__version__,

    author='hbc',
    author_email='bcxxxxxx@gmail.com',
    url='https://github.com/bcho/check',

    description='Check your server like a boss.',
    long_description='\n'.join((README, CHANGES)),
    license='SMPPL',

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'arrow',
        'click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        check=check.cli:main
    ''',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
    ]
)
