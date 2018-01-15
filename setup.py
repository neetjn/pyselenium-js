from setuptools import setup

setup(
    name='pyseleniumjs',
    description='Small library with javascript utilities for official Python selenium bindings.',
    version='1.3.7',
    url='https://neetjn.github.io/pyselenium-js/',
    author='John Nolette',
    author_email='john@neetgroup.net',
    license='Apache2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=[
        'selenium>=3.6.0',
        'six'
    ],
    packages=['pyseleniumjs']
)
