from setuptools import setup, find_packages

setup(
    name='loa',
    version='0.0.2',
    description='League of Artists',
    url='http://github.com/daew0n/loa',
    author='Daewon Lee',
    author_email='dwlee@cau.ac.kr',      
    packages=find_packages(),
    package_data={
        'loa': [
            'constraints/*.yml'
    ]},
    zip_safe=False
)