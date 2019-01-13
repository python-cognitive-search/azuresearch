from setuptools import setup

setup(
    name='azure_search',
    version='0.0.1',
    packages=['azuresearch', 'azuresearch.indexes', 'azuresearch.skills', 'azuresearch.analyzers'],
    url='https://github.com/omri374/python-azure-search',
    license='MIT',
    author='Samuel Spencer, Omri Mendels, Elad Iwanir',
    author_email='omri.mendels@microsoft.com',
    description='Python package for calling Azure Search and Azure Cognitive Search',
    install_requires=['requests'],
    test_requires=['haikunator', 'httpretty']
)
