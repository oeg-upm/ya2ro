################### SCHEMAS ###################################

from dataclasses import asdict, dataclass

class Iterable(object):
    def __iter__(self):
        return iter(asdict(self))

@dataclass(unsafe_hash=True)
class Contact:
    email: str = None
    phone: str = None

@dataclass(unsafe_hash=True)
class Project(Iterable):
    requirements: list = ("goal","social_motivation","sketch","areas","authors")
    title: str = None
    goal: str = None
    social_motivation: str = None
    sketch: str = None
    areas: list = None
    activities: list = None
    demo: str = None
    datasets: list = None
    software: list = None
    bibliography: list = None
    authors: list = None
    contact: Contact = None

@dataclass(unsafe_hash=True)
class Paper(Iterable):
    requirements: list = ("title","summary","datasets","authors")
    doi_paper: str = None
    title: str = None
    summary: str = None
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
    license: str = None
    
@dataclass(unsafe_hash=True)
class Demo:
    link: str = None
    name: str = None
    description: str = None

@dataclass(unsafe_hash=True)
class Bibliography_entry:
    entry: str = None



######################## FUNCTIONS #################################


import yaml 
from yaml.loader import SafeLoader
from pathlib import Path
import os
import sys
import req_orcid
import req_doi
import somef.cli
import properties as p
import json


def load_jsonld(input_jsonld):

    # Parse jsonld
    with open(Path(input_jsonld)) as file:
        jsonld_str = file.read()

    jsonld = json.loads(jsonld_str)

    for entry in jsonld["@graph"]:
        if entry["@id"] == "./":
            root = entry
            break
    
    for entry in root["hasPart"]:
        if str(entry["@id"]).endswith(".html"):
            index_html = entry["@id"]
            break
    
    type = root["DataType"]

    if type == "project":

        project = Project(
            title = root["name"],
            goal = root["description"]
        )

        # Meta info
        project.type = type
        project.index_html = index_html

        return project

    if type == "paper":
        paper = Paper(
            title = root["name"],
            summary = root["description"]
        )

        # Meta info
        paper.type = type
        paper.index_html = index_html

        return paper


def load_yaml(input_yaml):

    output_directory_datafolder = Path(p.output_directory, str(Path(input_yaml).stem))

    if not os.path.exists(output_directory_datafolder):
        os.makedirs(output_directory_datafolder)
        print(f"Creating output diretory {output_directory_datafolder}")

    # Create htaccess file
    import htaccess
    htaccess.create_htaccess(output_directory_datafolder)

    # Create images directory inside output folder
    images_output_path = Path(output_directory_datafolder, p.input_to_vocab["images"])
    if not os.path.exists(images_output_path):
        os.makedirs(images_output_path)
        print(f"Creating images diretory {output_directory_datafolder}/images")

    # Open input.yaml and parse it
    with open(Path(input_yaml)) as file:
        data = yaml.load(file, Loader=SafeLoader)
    
    print(f"Parsing and fetching info from {input_yaml}...\n")

    type = _safe(p.input_to_vocab["type"], data)
     
    if type not in ["paper", "project"]:
        print("""ERROR: Is required to specify a type field in the input yaml. Options: 'paper', 'project'.
       type: "paper"
       type: "project" """)
        exit()
    
    if type == "paper":
        data = init_paper(p.input_to_vocab, data)
        
    if type == "project":
        data = init_project(p.input_to_vocab, data)

    # Init data meta properties
    data.output_html = Path(output_directory_datafolder, p.properties["output_html"])
    data.output_html_help = Path(output_directory_datafolder, p.properties["output_html_help"])
    data.output_jsonld = Path(output_directory_datafolder, p.properties["output_jsonld"])
    data.output_directory_datafolder = output_directory_datafolder
    data.type = type
    data.yaml_file = input_yaml

    return data


def init_project(input_to_vocab, data):

    project = Project(
        title = _safe(input_to_vocab["title"], data),
        goal = _safe(input_to_vocab["goal"], data),
        social_motivation = _safe(input_to_vocab["social_motivation"], data),
        sketch = _safe(input_to_vocab["sketch"], data),
        areas = _safe(input_to_vocab["areas"], data),
        activities = _safe(input_to_vocab["activities"], data),
        demo = _list_empty_instances(Demo, input_to_vocab["demo"], data),
        datasets = _list_empty_instances(Dataset, input_to_vocab["datasets"], data),
        software = _list_empty_instances(Software, input_to_vocab["software"], data),
        bibliography = _list_empty_instances(Bibliography_entry, input_to_vocab["bibliography"], data),
        authors = _list_empty_instances(Author, input_to_vocab["participants"], data),
    )

    if project.title:
        print("    - Title: Done.")

    if project.goal:
        print("    - Goal: Done.")

    if project.social_motivation:
        print("    - Social motivation: Done.")

    if project.sketch:
        print("    - Sketch: Done.")
    
    if project.areas:
        print("    - Areas: Done.")
    
    if project.activities:
        print("    - Activities: Done.")

    # Demo
    populate_demo(project, input_to_vocab, data)

    # Datasets
    populate_datasets(project, input_to_vocab, data)

    # Software
    populate_software(project, input_to_vocab, data)
    
    # Bibliography
    populate_bibliography(project, input_to_vocab, data)

    # Authors
    populate_authors(project, input_to_vocab, data, field_of_author = "participants")

    # Contact
    populate_contact(project, input_to_vocab, data)

    return project


def init_paper(input_to_vocab, data):

    # Create paper object and pupulate the lists with empty instances
    paper = Paper(
        title = _safe(input_to_vocab["title"], data),
        summary = _safe(input_to_vocab["summary"], data),
        datasets = _list_empty_instances(Dataset, input_to_vocab["datasets"], data),
        software = _list_empty_instances(Software, input_to_vocab["software"], data),
        bibliography = _list_empty_instances(Bibliography_entry, input_to_vocab["bibliography"], data),
        authors = _list_empty_instances(Author, input_to_vocab["authors"], data),
    )

    if paper.title:
        print("    - Title: Done.")

    if paper.summary:
        print("    - Summary: Done.")

    # Datasets
    populate_datasets(paper, input_to_vocab, data)

    # Software
    populate_software(paper, input_to_vocab, data)
    
    # Bibliography
    populate_bibliography(paper, input_to_vocab, data)

    # Authors
    populate_authors(paper, input_to_vocab, data)
    
    # DOI Paper, get bib
    doi_paper_link = _safe(input_to_vocab["doi_paper"], data)
    if doi_paper_link is not None:
        print(f"    - Fetching data from {doi_paper_link}.")
        paper_bib = req_doi.bib(doi_paper_link)

        if paper.title is None:
            print(f"        + Fetching title from {doi_paper_link}.")
            paper.title = paper_bib.get_title()
        
        if paper.summary is None:
            print(f"        + Fetching summary from {doi_paper_link}.")
            paper.summary = paper_bib.get_summary()

        # TODO: Add authors with bib
    
    return paper
    

def _list_empty_instances(class_to_insatnce, key, dict):

    list_data = _safe(key, dict) 
    if list_data is None:
        return None

    return [class_to_insatnce() for _ in range(len(list_data))]
    

def _safe(key, dic):
    """Safe call to a dictionary. Returns value or None if key or dictionary does not exist"""
    if dic is not None and key in dic:
        return dic[key]
    else:
        return None
    

def populate_datasets(object, input_to_vocab, data):

    if object.datasets is None:
        return

    i = 0
    for dataset in data[input_to_vocab["datasets"]]:

        doi_dataset = _safe(input_to_vocab["doi_dataset"], dataset)
        if doi_dataset is not None:
            object.datasets[i].doi_dataset = doi_dataset
            
        link = _safe(input_to_vocab["link"], dataset)
        if link is not None:
            object.datasets[i].link = link

        name = _safe(input_to_vocab["name"], dataset)
        if name is not None:
            object.datasets[i].name = name 
        
        descripton = _safe(input_to_vocab["description"], dataset)
        if descripton is not None:
            object.datasets[i].description = descripton

        i += 1
    print("    - Datasets: Done.")


def populate_software(object, input_to_vocab, data):

    if object.software is None:
        return

    i = 0
    for software in data[input_to_vocab["software"]]:
        link = _safe(input_to_vocab["link"], software)
        
        if link is not None:
            object.software[i].link = link

            if link.startswith("https://github.com/"):

                print(f"        + Using SOMEF for {link}")
                header = {}
                header['accept'] = 'application/vnd.github.v3+json'

                with HiddenPrints():
                    _, github_data = somef.cli.load_repository_metadata(link, header)

                object.software[i].name = _safe("name", github_data)
                object.software[i].description = _safe("description", github_data)
                object.software[i].license = _safe("name",_safe("license", github_data))

        name = _safe(input_to_vocab["name"], software)
        if name is not None:
            object.software[i].name = name
        
        description = _safe(input_to_vocab["description"], software)
        if description is not None:
            object.software[i].description = description
        
        license = _safe(input_to_vocab["license"], software)
        if license is not None:
            object.software[i].license = license

        i += 1
    print("    - Software: Done.")


def populate_demo(object, input_to_vocab, data):

    if object.demo is None:
        return

    i = 0
    for demo in data[input_to_vocab["demo"]]:

        link = _safe(input_to_vocab["link"], demo)
        if link is not None:
            object.demo[i].link = link
        
        name = _safe(input_to_vocab["name"], demo)
        if name is not None:
            object.demo[i].name = name
        
        description = _safe(input_to_vocab["description"], demo)
        if description is not None:
            object.demo[i].description = description

        i += 1
        
    print("    - Demo: Done.")


def populate_bibliography(object, input_to_vocab, data):

    if object.bibliography is None:
        return None

    i = 0
    for entry in data[input_to_vocab["bibliography"]]:

        object.bibliography[i].entry = entry

        i += 1
    print("    - Bibliography: Done.")


def populate_contact(object, input_to_vocab, data):

    contact = _safe(input_to_vocab["contact"], data)
    if contact is None:
        return None

    phone = _safe(input_to_vocab["phone"], contact)
    email = _safe(input_to_vocab["email"], contact)

    if phone and email:
        object.contact = Contact(email, phone)
        print("    - Contact: Done.")

    else:
        print("ERROR: Contact phone and/or email are not decalred.")
        exit()


def populate_authors(object, input_to_vocab, data, field_of_author = "authors"):

    if object.authors is None:
        return None

    i = 0
    for author in data[input_to_vocab[field_of_author]]:

        name = None
        # Orcid implementation
        orcid_link = _safe(input_to_vocab["orcid"], author)
        if orcid_link is not None:
            print(f"        + Fetching author data from {orcid_link}.")
            orcid = req_orcid.orcid(orcid_link)
            object.authors[i].orcid = orcid_link
            name = orcid.get_full_name()
            object.authors[i].name = name
            object.authors[i].position = ", ".join(orcid.get_affiliation())
            object.authors[i].web = orcid.get_webs()[-1]
            object.authors[i].description = orcid.get_bio()
        
        aux = _safe(input_to_vocab["name"], author)
        name =  aux if aux is not None else name
        if name is not None:
            object.authors[i].name = name
        
        photo = _safe(input_to_vocab["photo"], author)
        if photo is not None:
            object.authors[i].photo = photo
        else:
            print(f"        + Using default photo for {name}.")
            object.authors[i].photo = input_to_vocab["images"] + "/" + p.properties["default_author_img"]
        
        position = _safe(input_to_vocab["position"], author)
        if position is not None:
            object.authors[i].position = position
        
        description = _safe(input_to_vocab["description"], author)
        if description is not None:
            object.authors[i].description = description
        
        web = _safe(input_to_vocab["web"], author)
        if web is not None:
            object.authors[i].web = web
        
        role = _safe(input_to_vocab["role"], author)
        if role is not None:
            object.authors[i].role = role
        else:
            object.authors[i].role = "Author"
        
        i += 1
    print("    - Authors: Done.")


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
