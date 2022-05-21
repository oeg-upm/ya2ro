from setuptools import find_packages, setup
from src.ya2ro.ya2ro import __version__

setup(
    name='ya2ro',
    author='Antonia Pavel',
    author_email='floriana.antonia.pavel@gmail.com',
    description='Tool to which you pass basic information of a project or a research article (such as the datasets, software, people who have been involved, bibliography...) and generates two files with structured information with the intention of easing the readability for machines and people. One file is a webpage with all the relevant information and the other one is a Research Object.',
    version=__version__,
    url='https://github.com/oeg-upm/ya2ro',
    packages=find_packages(where="src",),
    package_dir={"": "src"},
    package_data={'ya2ro': ['images/*', 'resources/*']},
    license='Apache License 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'ya2ro = ya2ro.ya2ro:main',
        ],
    },
    install_requires=[
        'PyYAML>=5.0.0',
        'bs4>=0.0.1',
        'requests>=2.22.0',
        'bibtexparser>=1.2.0',
        'Pygments>=2.11.2',
        'somef>=0.8.0',
        'scc @ git+https://github.com/oeg-upm/soca',
        'metadata-parser'
    ]
)
