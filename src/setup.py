import os
from setuptools import setup, find_packages


def list_requirements(file_name):
    """ Converting requirements.txt into list"""
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    with open(file_path, 'r') as f:
        return f.read().split()


PACKAGE_NAME = 'test_app'

setup(
    name=PACKAGE_NAME,
    version='0.0.0',
    packages=find_packages(where=''),
    package_data={PACKAGE_NAME: ["*.sql", "*.html"]},
    include_package_data=True,
    install_requires=list_requirements('requirements.txt'),
    tests_require=list_requirements('test-requirements.txt'),
    extras_require={
        'test':  list_requirements('test-requirements.txt'),
    }
)
