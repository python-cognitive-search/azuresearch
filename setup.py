"""
Setup
"""
from setuptools import setup

with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

setup(
    name='azure_search',
    version='0.0.3',
    packages=['azuresearch', 'azuresearch.indexes',
              'azuresearch.skills', 'azuresearch.analyzers'],
    url='https://github.com/python-cognitive-search/azuresearch',
    license='MIT',
    author='Samuel Spencer, Omri Mendels, Elad Iwanir',
    author_email='omri.mendels@microsoft.com',
    description='Python package for calling Azure Search and Azure Cognitive Search',
    install_requires=REQUIRED)
