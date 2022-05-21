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
    requirements: list = ("title","goal","areas","software","authors")
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
    requirements: list = ("title","summary","datasets","bibliography","authors")
    doi_paper: str = None
    title: str = None
    summary: str = None
    datasets: list = None
    software: list = None
    bibliography: list = None
    authors: list = None
    bib: object = None

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
    doi: str = None
    link: str = None
    name: str = None
    description: str = None
    license: str = None
    author: str = None
    path: str = None

@dataclass(unsafe_hash=True)
class Software:
    metadata: dict = None
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

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


import yaml 
from yaml.loader import SafeLoader
from pathlib import Path
import os
import sys
from . import req_orcid
from . import req_doi
from somef.cli import cli_get_data
from . import properties as p
import json
from shutil import copyfile
from scc.commands.portal.metadata import metadata as scc_metadata
import warnings
warnings.filterwarnings("ignore")
import metadata_parser



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
    
    type = str(root["DataType"]).lower()
    

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

    global output_directory_datafolder

    output_directory_datafolder = Path(p.output_directory, str(Path(input_yaml).stem))

    if not os.path.exists(output_directory_datafolder):
        os.makedirs(output_directory_datafolder)
        print(f"Creating output directory {output_directory_datafolder}")

    # Create htaccess file
    from . import htaccess
    htaccess.create_htaccess(output_directory_datafolder)

    # Create images directory inside output folder
    images_output_path = Path(output_directory_datafolder, p.input_to_vocab["images"])
    if not os.path.exists(images_output_path):
        os.makedirs(images_output_path)
        print(f"Creating images directory {output_directory_datafolder}/images")

    # Open input.yaml and parse it
    with open(Path(input_yaml)) as file:
        data = yaml.load(file, Loader=SafeLoader)
    
    print(f"Parsing and fetching info from {input_yaml}\n")

    type = _safe(p.input_to_vocab["type"], data)
    if type:
        del data["type"]
     
    if type not in ["paper", "project"]:
        print("""ERROR: Is required to specify a type field in the input yaml. Options: 'paper', 'project'.
       type: "paper"
       type: "project" """)
        exit()
    
    if type == "paper":
        init_data = init_paper(p.input_to_vocab, data)
        
    if type == "project":
        init_data = init_project(p.input_to_vocab, data)

    # Init data meta properties
    init_data.output_html = Path(output_directory_datafolder, p.properties["output_html"])
    init_data.output_html_help = Path(output_directory_datafolder, p.properties["output_html_help"])
    init_data.output_jsonld = Path(output_directory_datafolder, p.properties["output_jsonld"])
    init_data.output_directory_datafolder = output_directory_datafolder
    init_data.type = type
    init_data.yaml_file = input_yaml

    # Check for not supported fields
    for uninit_data in data.keys():
        print(f"\nERROR: The field '{uninit_data}' is not supported or is misspelled. Check out our documentation https://github.com/oeg-upm/ya2ro/blob/main/doc.md")

    return init_data


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
        del data["title"]


    if project.goal:
        print("    - Goal: Done.")
        del data["goal"]
        

    if project.social_motivation:
        print("    - Social motivation: Done.")
        del data["social_motivation"]

    if project.sketch:
        print("    - Sketch: Done.")
        del data["sketch"]

    if project.areas:
        print("    - Areas: Done.")
        del data["areas"]
    
    if project.activities:
        print("    - Activities: Done.")
        del data["activities"]

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

    # Create paper object and populate the lists with empty instances
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
        del data["title"]

    if paper.summary:
        print("    - Summary: Done.")
        del data["summary"]


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

        try:
            paper_bib = req_doi.bib(doi_paper_link)

            if paper.title is None:
                print(f"        + Fetching title from {doi_paper_link}.")
                paper.title = paper_bib.get_title()
            
            if paper.summary is None:
                print(f"        + Fetching summary from {doi_paper_link}.")
                paper.summary = paper_bib.get_summary()

            # Add bibtext
            paper.bib = paper_bib.get_bibtext()

            # Add citation
            citation = paper_bib.get_citation()
            if citation:

                if not paper.bibliography:
                    paper.bibliography = []
                    
                paper.bibliography.append(
                    Bibliography_entry(entry = citation)
                    )

            # Add authors with DOI
            doi_authors = paper_bib.get_authors()
            if doi_authors:
                for doi_author in doi_authors:
                    if not paper.authors or doi_author not in [ a.name for a in paper.authors ]:

                        print(f"        + Author: {doi_author} extracted from {doi_paper_link}.")
                        print(f"        + Using default photo for {doi_author}.")

                        # TODO: Add more data for new authors

                        if not paper.authors:
                            paper.authors = []

                        paper.authors.append(Author(
                            name = doi_author, 
                            photo = Path(input_to_vocab["images"], p.properties["default_author_img"]),
                            role= "Author"
                        ))
        except:
            print(f"ERROR: doi_paper is not valid '{doi_paper_link}'")

        del data["doi_paper"]
                    
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
        
        if isinstance(dataset, dict):
            doi = _safe(input_to_vocab["doi"], dataset)
            path = _safe(input_to_vocab["path"], dataset)
            link = _safe(input_to_vocab["link"], dataset)
        elif isinstance(dataset, str):
            if 'doi' in dataset:
                doi = dataset
            else:
                link = dataset
                doi = None
        else:
            print(f"WARNING: {dataset} format is not supported, see documentation for further guidance.")
            

        if doi:

            object.datasets[i].doi = doi
            object.datasets[i].link = doi

            try:
                req_d = req_doi.dataset(doi)
                print(f"        + Fetching dataset data from {doi}")
                object.datasets[i].description = req_d.get_description()
                object.datasets[i].name = req_d.get_name()
                object.datasets[i].license = req_d.get_license()
                object.datasets[i].author = req_d.get_author()

            except:
                print(f"ERROR: {doi} is not a DOI. Use the field 'link' or 'path' instead.")

        elif path:
            object.datasets[i].path = path
            object.datasets[i].files = []

            # Create datasets directory inside output folder
            datasets_output_path = Path(output_directory_datafolder, "datasets")
            if not os.path.exists(datasets_output_path):
                os.makedirs(datasets_output_path)
                print(f"Creating datasets directory {datasets_output_path}")

            if os.path.isdir(path):
                directory = os.fsencode(path)
                for file in os.listdir(directory):
                    # copy dataset to output/images directory
                    filename = os.fsdecode(file)
                    src = Path(path,filename)
                    dst = Path(datasets_output_path, filename)
                    copyfile(src, dst)
                    object.datasets[i].files.append(f"datasets/{filename}")
            elif os.path.isfile(path):
                # copy dataset to output/images directory
                src = Path(path)
                filename = os.path.basename(src)
                dst = Path(datasets_output_path, filename)
                copyfile(src, dst)
                object.datasets[i].files.append(f"datasets/{filename}")
            else:
                print(f"ERROR: {path} does not exist.")

        elif link:
            object.datasets[i].link = link
            try:
                page = metadata_parser.MetadataParser(url=link)
                print(f"        + Trying to extract metadata from {link}.")
                object.datasets[i].description = page.get_metadata('description')
                object.datasets[i].name = page.get_metadata('title')
                object.datasets[i].license = page.get_metadata('license')
            except:
                print(f"WARNING: No metadata could be extracted from {link}")

            
        name = _safe(input_to_vocab["name"], dataset)
        if name:
            object.datasets[i].name = name 
        
        description = _safe(input_to_vocab["description"], dataset)
        if description:
            object.datasets[i].description = description
        
        license = _safe(input_to_vocab["license"], dataset)
        if license:
            object.dataset[i].license = license
        
        author = _safe(input_to_vocab["author"], dataset)
        if author:
            object.dataset[i].author = author
    
        i += 1
    print("    - Datasets: Done.")
    del data["datasets"]


def populate_software(object, input_to_vocab, data):

    if object.software is None:
        return

    i = 0
    for software in data[input_to_vocab["software"]]:

        if isinstance(software, str) and 'http' in software:
            link = software
        else:
            link = _safe(input_to_vocab["link"], software)
        
        if link is not None:
            object.software[i].link = link

            if link.startswith("https://github.com/") and not p.no_somef:

                print(f"        + Using SOMEF for {link}")
                print("            - Downloading repository... This may take a while.")
                with HiddenPrints():
                    metadata = cli_get_data(0.9, False, link)
                
                scc_meta = scc_metadata(output_directory_datafolder, metadata)
                object.software[i].metadata = metadata
                object.software[i].name = scc_meta.title()
                object.software[i].description = scc_meta.description()
                license = scc_meta.license()
                if license:
                    license = license['name']
                object.software[i].license = scc_meta.license()

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
    del data["software"]


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
    del data["demo"]


def populate_bibliography(object, input_to_vocab, data):

    if object.bibliography is None:
        return None

    i = 0
    for entry in data[input_to_vocab["bibliography"]]:
        try:
            paper_bib = req_doi.bib(entry)
            print(f"        + Fetching bibliography entry from {entry}.")
            object.bibliography[i].entry = paper_bib.get_citation()
        except:
            object.bibliography[i].entry = entry

        i += 1
    print("    - Bibliography: Done.")
    del data["bibliography"]


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

    del data["contact"]
    

def populate_authors(object, input_to_vocab, data, field_of_author = "authors"):

    if object.authors is None:
        return None

    i = 0
    for author in data[input_to_vocab[field_of_author]]:

        name = None
        # Orcid implementation
        orcid_link = _safe(input_to_vocab["orcid"], author)
        if orcid_link is not None:
            try:
                orcid = req_orcid.orcid(orcid_link)
                print(f"        + Fetching author data from {orcid_link}.")
                object.authors[i].orcid = orcid_link
                name = orcid.get_full_name()
                object.authors[i].name = name
                aff = orcid.get_affiliation()
                if aff:
                    object.authors[i].position = ", ".join(aff)
                webs = orcid.get_webs()
                if webs:
                    object.authors[i].web = webs[-1]
                object.authors[i].description = orcid.get_bio()
            except:
                print(f"ERROR: ORCID is not valid or not up '{orcid_link}'")
            
        aux = _safe(input_to_vocab["name"], author)
        name =  aux if aux is not None else name
        if name is not None:
            object.authors[i].name = name
        
        photo = _safe(input_to_vocab["photo"], author)
        if photo is not None:
            object.authors[i].photo = photo
        else:
            print(f"        + Using default photo for {name}.")
            object.authors[i].photo = Path(input_to_vocab["images"], p.properties["default_author_img"])
        
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
    del data[field_of_author]
