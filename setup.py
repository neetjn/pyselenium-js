from setuptools import setup, find_packages

setup(
    name='pyseleniumjs',
    description='Small library with javascript utilities for official Python selenium bindings.',
    version='1.0.2b7',
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
    packages=find_packages()
)