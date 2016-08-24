#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name='django-planfix',
    version='0.1',
    description='Add contanct and task to Planfix',
    author='Mikhail Maltsev',
    author_email='drumsland@gmail.com',
    url='https://github.com/chadoneba/django-planfix',
    long_description=open('README.rst', 'r').read(),
    packages=[
        'planfix',
    ],
    zip_safe=False,
    requires=[
        'requests',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
)