"""Setup for dependencies for iiif-ld-demo."""
from setuptools import setup

setup(
    name='iiif-ld-demo',
    author='Simeon Warner',
    author_email='simeon.warner@cornell.edu',
    packages=[],
    scripts=[],
    url='https://github.com/zimeon/iiif-ld-demo',
    description='IIIF Linked Data Demo',
    long_description=open('README.md').read(),
    install_requires=[
        'rdflib>=4.2.0',
        'rdflib-jsonld',
        'pyld',
        'json_delta'
    ],
    test_suite="tests",
    tests_require=[
        'pytest>=2.7.3',
        'misaka',
        'command'
    ]
)
