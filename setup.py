from setuptools import setup

setup(
    name='pyselenium-js',
    description='Small library with javascript utilities for official Python selenium bindings.',
    version='1.0.0b2',
    url='https://github.com/neetVeritas/pyselenium-js',
    author='John Nolette',
    author_email='john@neetgroup.net',
    license='Apache2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=[
        'selenium>=3.0.0b3'
    ]
)