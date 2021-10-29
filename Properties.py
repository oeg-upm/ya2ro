import yaml 
from yaml.loader import SafeLoader
from pathlib import Path
import os
import data_wrapper
import req_orcid
import req_doi

def init(properties_file, input_yalm, output_directory_param):
    global properties, output_directory, data, style

    # Make visible output directoty to all modules
    output_directory = output_directory_param

    # Create paths for output files
    with open(Path(properties_file)) as file:
        properties = yaml.load(file, Loader=SafeLoader)

    properties["output_html"] = Path(output_directory +"/"+ properties["output_html"])
    properties["output_jsonld"] = Path(output_directory +"/"+ properties["output_jsonld"])

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
    images_output_path = Path(output_directory + "/" + input_to_vocab["images"])
    if not os.path.exists(images_output_path):
        os.makedirs(images_output_path)
        print(f"Creating images diretory {output_directory}")

    # Open input.yalm and parse it
    with open(Path(input_yalm)) as file:
        data = yaml.load(file, Loader=SafeLoader)
    
    print(f"Parsing and fetching info from {input_yalm}...")

    # Style selector
    style = _safe(input_to_vocab["style"], data)
    style = style if style else "default"

    type = _safe(input_to_vocab["type"], data)
     
    if type is None:
        print("""ERROR: Is required to specify a type field in the input yalm. Options: 'paper', 'project'.
       type: "paper"
       type: "project" """)
        exit()

    if type == "paper":
        data = init_paper(input_to_vocab, data)
        
    if type == "project":
        data = init_project(input_to_vocab, data)
    
def init_project(input_to_vocab, data):

    project = data_wrapper.Project(
        title = _safe(input_to_vocab["title"], data),
        goal = _safe(input_to_vocab["goal"], data),
        social_motivation = _safe(input_to_vocab["social_motivation"], data),
        sketch = _safe(input_to_vocab["sketch"], data),
        areas = _safe(input_to_vocab["areas"], data),
        demo = [data_wrapper.Demo() for _ in range(len(data[input_to_vocab["demo"]]))],
        datasets = [data_wrapper.Dataset() for _ in range(len(data[input_to_vocab["datasets"]][input_to_vocab["datasets_links"]]))],
        doi_datasets = _safe(input_to_vocab["doi_datasets"], data[input_to_vocab["datasets"]]),
        software = [data_wrapper.Software() for _ in range(len(data[input_to_vocab["software"]]))],
        bibliography = [data_wrapper.Bibliography_entry() for _ in range(len(data[input_to_vocab["bibliography"]]))],
        authors = [data_wrapper.Author() for _ in range(len(data[input_to_vocab["participants"]]))]
    )
    
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

    # Create paper objetc and pupulate the lists with empty instances
    paper = data_wrapper.Paper(
        title = _safe(input_to_vocab["title"], data),
        summary = _safe(input_to_vocab["summary"], data),
        datasets = [data_wrapper.Dataset() for _ in range(len(data[input_to_vocab["datasets"]][input_to_vocab["datasets_links"]]))],
        doi_datasets = _safe(input_to_vocab["doi_datasets"], data[input_to_vocab["datasets"]]),
        software = [data_wrapper.Software() for _ in range(len(data[input_to_vocab["software"]]))],
        bibliography = [data_wrapper.Bibliography_entry() for _ in range(len(data[input_to_vocab["bibliography"]]))],
        authors = [data_wrapper.Author() for _ in range(len(data[input_to_vocab["authors"]]))]
    )

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
    

def _safe(key, dic):
    """Safe call to a dictionary. Returns value or None if key does not exist"""
    if key in dic:
        return dic[key]
    else:
        return None
    
def populate_datasets(object, input_to_vocab, data):
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
    i = 0
    for software in data[input_to_vocab["software"]]:
        link = _safe(input_to_vocab["link"], software)
        if link is not None:
            object.software[i].link = link
        
        name = _safe(input_to_vocab["name"], software)
        if name is not None:
            object.software[i].name = name
        
        description = _safe(input_to_vocab["description"], software)
        if description is not None:
            object.software[i].description = description
        i += 1
    print("    - Software: Done.")
    
def populate_demo(object, input_to_vocab, data):
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

def populate_bibliography(paper, input_to_vocab, data):
    i = 0
    for entry in data[input_to_vocab["bibliography"]]:

        paper.bibliography[i].entry = entry

        i += 1
    print("    - Bibliography: Done.")

def populate_authors(object, input_to_vocab, data, field_of_author = "authors"):
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
        
        i += 1
    print("    - Authors: Done.")

