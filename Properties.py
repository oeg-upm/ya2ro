import yaml 
from yaml.loader import SafeLoader
from pathlib import Path
import os
import sys
import data_wrapper
import req_orcid
import req_doi
import somef.cli

def init(properties_file, input_yalm, output_directory_param):
    global properties, output_directory, style

    # Make visible output directoty to all modules
    output_directory = output_directory_param

    # Create paths for output files
    with open(Path(properties_file)) as file:
        properties = yaml.load(file, Loader=SafeLoader)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Creating output diretory {output_directory}")

    # Create htaccess file
    import htaccess
    htaccess.create_htaccess()

    # Load vocab used in the input.yalm
    with open(Path(properties["input_to_vocab_yaml"])) as file:
        input_to_vocab = yaml.load(file, Loader=SafeLoader)

    # Create images directory inside output folder
    images_output_path = Path(output_directory, input_to_vocab["images"])
    if not os.path.exists(images_output_path):
        os.makedirs(images_output_path)
        print(f"Creating images diretory {output_directory}")

    # Open input.yalm and parse it
    with open(Path(input_yalm)) as file:
        data = yaml.load(file, Loader=SafeLoader)
    
    print(f"Parsing and fetching info from {input_yalm}...\n")

    # Style selector
    style = _safe(input_to_vocab["style"], properties)
    style = style if style else "default"

    type = _safe(input_to_vocab["type"], data)
     
    if type not in ["paper", "project"]:
        print("""ERROR: Is required to specify a type field in the input yalm. Options: 'paper', 'project'.
       type: "paper"
       type: "project" """)
        exit()
    
    if type == "paper":
        data = init_paper(input_to_vocab, data)
        
    if type == "project":
        data = init_project(input_to_vocab, data)

    # Init data meta properties
    data.output_html = Path(output_directory, properties["output_html"])
    data.output_html_help = Path(output_directory, properties["output_html_help"])
    data.output_jsonld = Path(output_directory, properties["output_jsonld"])
    data.type = type

    return data


def init_project(input_to_vocab, data):

    project = data_wrapper.Project(
        title = _safe(input_to_vocab["title"], data),
        goal = _safe(input_to_vocab["goal"], data),
        social_motivation = _safe(input_to_vocab["social_motivation"], data),
        sketch = _safe(input_to_vocab["sketch"], data),
        areas = _safe(input_to_vocab["areas"], data),
        demo = _list_empty_instances(data_wrapper.Demo, input_to_vocab["demo"], data),
        datasets = _list_empty_instances(data_wrapper.Dataset, input_to_vocab["datasets_links"], _safe(input_to_vocab["datasets"], data)),
        doi_datasets = _safe(input_to_vocab["doi_datasets"], _safe(input_to_vocab["datasets"], data)),
        software = _list_empty_instances(data_wrapper.Software, input_to_vocab["software"], data),
        bibliography = _list_empty_instances(data_wrapper.Bibliography_entry, input_to_vocab["bibliography"], data),
        authors = _list_empty_instances(data_wrapper.Author, input_to_vocab["participants"], data),
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

    return project


def init_paper(input_to_vocab, data):

    # Create paper object and pupulate the lists with empty instances
    paper = data_wrapper.Paper(
        title = _safe(input_to_vocab["title"], data),
        summary = _safe(input_to_vocab["summary"], data),
        datasets = _list_empty_instances(data_wrapper.Dataset, input_to_vocab["datasets_links"], _safe(input_to_vocab["datasets"], data)),
        doi_datasets = _safe(input_to_vocab["doi_datasets"], _safe(input_to_vocab["datasets"], data)),
        software = _list_empty_instances(data_wrapper.Software, input_to_vocab["software"], data),
        bibliography = _list_empty_instances(data_wrapper.Bibliography_entry, input_to_vocab["bibliography"], data),
        authors = _list_empty_instances(data_wrapper.Author, input_to_vocab["authors"], data),
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
        print(f"    - Fetching data fom {doi_paper_link}.")
        paper_bib = req_doi.bib(doi_paper_link)

        if paper.title is None:
            print(f"        + Fetching title fom {doi_paper_link}.")
            paper.title = paper_bib.get_title()
        
        if paper.summary is None:
            print(f"        + Fetching summary fom {doi_paper_link}.")
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
    for dataset in data[input_to_vocab["datasets"]][input_to_vocab["datasets_links"]]:

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

            # SOMEF: TODO: Extract more useful data
            if link.startswith("https://github.com/"):

                print(f"        + Using SOMEF for {link}")
                header = {}
                header['accept'] = 'application/vnd.github.v3+json'

                with HiddenPrints():
                    text, github_data = somef.cli.load_repository_metadata(link, header)

                #print("Text: ", text)
                #print("Github_data: ", github_data.keys())
                #print("Github_data: ", github_data)

                object.software[i].name = github_data["name"]
        
        name = _safe(input_to_vocab["name"], software)
        if name is not None:
            object.software[i].name = name
        
        description = _safe(input_to_vocab["description"], software)
        if description is not None:
            object.software[i].description = description
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

def populate_authors(object, input_to_vocab, data, field_of_author = "authors"):

    if object.authors is None:
        return None

    i = 0
    for author in data[input_to_vocab[field_of_author]]:

        name = None
        # Orcid implementation
        orcid_link = _safe(input_to_vocab["orcid"], author)
        if orcid_link is not None:
            print(f"        + Fetching author data fom {orcid_link}.")
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
            object.authors[i].photo = input_to_vocab["images"] + "/" + photo
        else:
            print(f"        + Using default photo for {name}.")
            object.authors[i].photo = input_to_vocab["images"] + "/" + properties["default_author_img"]
        
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