from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Paper:
    doi_paper: str = None
    title: str = None
    summary: str = None
    doi_datasets: str = None
    datasets: list = None
    software: list = None
    bibliography: list = None
    authors: list = None

@dataclass(unsafe_hash=True)
class Author:
    orcid: str = None
    name: str = None
    photo: str = None
    position: str = None
    description: str = None
    web: str = None

@dataclass(unsafe_hash=True)
class Dataset:
    doi_dataset: str = None
    link: str = None
    name: str = None
    description: str = None

@dataclass(unsafe_hash=True)
class Software:
    link: str = None
    name: str = None
    description: str = None

@dataclass(unsafe_hash=True)
class Bibliography_entry:
    entry: str = None


