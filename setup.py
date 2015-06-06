from codecs import open
from os import path

from setuptools import find_packages, setup


wd = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(wd, 'DESCRIPTION'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-blogsmith',
    version='0.1.0',

    description='A micro-blogging app for Django.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/sjberry/django-blogsmith',

    # Author details
    author='Steven Berry',
    author_email='steven@sberry.me',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],

    # What does your project relate to?
    keywords='blog blogging',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'requirements', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['django', 'dropbox', 'misaka', 'pygments'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
)
