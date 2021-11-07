from dataclasses import asdict, dataclass, asdict

class Iterable(object):
    def __iter__(self):
        return iter(asdict(self))

@dataclass(unsafe_hash=True)
class Project(Iterable):
    requirements: list = ("goal","social_motivation","sketch","areas","authors")
    title: str = None
    goal: str = None
    social_motivation: str = None
    sketch: str = None
    areas: list = None
    demo: str = None
    datasets: list = None
    doi_datasets: str = None
    software: list = None
    bibliography: list = None
    authors: list = None

@dataclass(unsafe_hash=True)
class Paper(Iterable):
    requirements: list = ("title","summary","datasets","authors")
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
    role: str = None

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
class Demo:
    link: str = None
    name: str = None
    description: str = None

@dataclass(unsafe_hash=True)
class Bibliography_entry:
    entry: str = None


