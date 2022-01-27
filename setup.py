from setuptools import find_packages, setup

setup(
    name='ya2ro',
    description='Tool to which you pass basic information of a project or a research article (such as the datasets, software, people who have been involved, bibliography...) and generates two files with structured information with the intention of easing the readability for machines and people. One file is a webpage with all the relevant information and the other one is a Research Object.',
    version='0.0.1',
    url='https://github.com/oeg-upm/ya2ro',
    packages=find_packages(include=['ya2ro', 'ya2ro.*']),
    package_dir={'ya2ro': 'src/ya2ro'},
    package_data={'ya2ro': ['/images', '/resources']},
    license='Version 2.0',
    long_description=open('README.txt').read(),
    install_requires=[
        'PyYAML>=6.0',
        'bs4>=0.0.1',
        'requests>=2.27.1',
        'bibtexparser>=1.2.0',
        'Pygments>=2.11.2',
        'somef>=0.6.0'
    ],
    python_requires=">=3.9"
)