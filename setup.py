from setuptools import setup

buildnum = "0.0.1"

readme = open('README.md').read()
requirements_file = open('requirements.txt')
requirements = requirements_file.read().strip().split('\n')
requirements_file.close()

setup(
    name='couch-crdt',
    version=buildnum,
    description='',
    author_email='simon@cloudant.com',
    long_description=readme,
    packages=['couchcrdt'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements
)
