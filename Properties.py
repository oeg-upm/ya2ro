import yaml 
from yaml.loader import SafeLoader
from pathlib import Path
import os
import data_wrapper
import req_orcid
import req_doi

def init(properties_file, input_yalm, output_directory_param):
    global properties, input_to_vocab, output_directory, paper

    # Make visible output directoty to all modules
    output_directory = output_directory_param

    # Create paths for output files
    with open(Path(properties_file)) as file:
        properties = yaml.load(file, Loader=SafeLoader)
    properties["output_html"] = Path(output_directory +"/"+ properties["output_html"])
    properties["output_jsonld"] = Path(output_directory +"/"+ properties["output_jsonld"])

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load vocab used in the input.yalm
    with open(Path(properties["input_to_vocab_yaml"])) as file:
        input_to_vocab = yaml.load(file, Loader=SafeLoader)

    # Create images directory inside output folder
    images_output_path = Path(output_directory + "/" + input_to_vocab["images"])
    if not os.path.exists(images_output_path):
        os.makedirs(images_output_path)

    # Open input.yalm and parse it
    with open(Path(input_yalm)) as file:
        data = yaml.load(file, Loader=SafeLoader)

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
    i = 0
    for dataset in data[input_to_vocab["datasets"]][input_to_vocab["datasets_links"]]:

        doi_dataset = _safe(input_to_vocab["doi_dataset"], dataset)
        if doi_dataset is not None:
            paper.datasets[i].doi_dataset = doi_dataset
            
        link = _safe(input_to_vocab["link"], dataset)
        if link is not None:
            paper.datasets[i].link = link

        name = _safe(input_to_vocab["name"], dataset)
        if name is not None:
            paper.datasets[i].name = name 
        
        descripton = _safe(input_to_vocab["description"], dataset)
        if descripton is not None:
            paper.datasets[i].description = descripton

        i += 1

    # Software
    i = 0
    for software in data[input_to_vocab["software"]]:

        link = _safe(input_to_vocab["link"], software)
        if link is not None:
            paper.software[i].link = link
        
        name = _safe(input_to_vocab["name"], software)
        if name is not None:
            paper.software[i].name = name
        
        description = _safe(input_to_vocab["description"], software)
        if description is not None:
            paper.software[i].description = description

        i += 1

    # Bibliography
    i = 0
    for entry in data[input_to_vocab["bibliography"]]:

        paper.bibliography[i].entry = entry

        i += 1
        
    
    # Authors
    i = 0
    for author in data[input_to_vocab["authors"]]:

        orcid_link = _safe(input_to_vocab["orcid"], author)
        if orcid_link is not None:
            orcid = req_orcid.orcid(orcid_link)
            paper.authors[i].orcid = orcid_link
            paper.authors[i].name = orcid.get_full_name()
            paper.authors[i].position = "\n".join(orcid.get_affiliation())
            paper.authors[i].web = orcid.get_webs()[-1]
            paper.authors[i].description = orcid.get_bio()

        name = _safe(input_to_vocab["name"], author)
        if name is not None:
            paper.authors[i].name = name
        
        photo = _safe(input_to_vocab["photo"], author)
        if photo is not None:
            paper.authors[i].photo = photo
        else:
            paper.authors[i].photo = input_to_vocab["images"] + "/" + properties["default_author_img"]
        
        position = _safe(input_to_vocab["position"], author)
        if position is not None:
            paper.authors[i].position = position
        
        description = _safe(input_to_vocab["description"], author)
        if description is not None:
            paper.authors[i].description = description
        
        web = _safe(input_to_vocab["web"], author)
        if web is not None:
            paper.authors[i].web = web
        
        i += 1
    
    # DOI Paper, get bib
    doi_paper_link = _safe(input_to_vocab["doi_paper"], data)
    if doi_paper_link is not None:
        paper_bib = req_doi.bib(doi_paper_link)

        if paper.title is None:
            paper.title = paper_bib.get_title()
        
        if paper.summary is None:
            paper.summary = paper_bib.get_summary()

        # TODO: Add authors with bib
        

def _safe(key, dic):
    """Safe call to a dictionary. Returns value or None if key does not exist"""
    if key in dic:
        return dic[key]
    else:
        return None
    


