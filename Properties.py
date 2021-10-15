import yaml 
from yaml.loader import SafeLoader
from pathlib import Path
import os
import data_wrapper

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
        title = data[input_to_vocab["title"]],
        summary = data[input_to_vocab["summary"]],
        datasets = [],
        doi_datasets = data[input_to_vocab["datasets"]][input_to_vocab["doi_datasets"]],
        software = [],
        bibliography = [],
        authors = []
    )

    # First use automated info from doi and orcid
    # TODO

    # Second use information provided by the user (ovrwrite any existing info)

    # Datasets
    for dataset in data[input_to_vocab["datasets"]][input_to_vocab["datasets_links"]]:
        paper.datasets.append(
            data_wrapper.Dataset(
                doi_dataset = dataset[input_to_vocab["doi_dataset"]],
                link = dataset[input_to_vocab["link"]],
                name = dataset[input_to_vocab["name"]],
                description = dataset[input_to_vocab["description"]]
            )
        )
    
    # Software
    for software in data[input_to_vocab["software"]]:
        paper.software.append(
            data_wrapper.Software(
                link = software[input_to_vocab["link"]],
                name = software[input_to_vocab["name"]],
                description = software[input_to_vocab["description"]]
            )
        )

    # Bibliography
    for entry in data[input_to_vocab["bibliography"]]:
        paper.bibliography.append(
            data_wrapper.Bibliography_entry(
                entry = entry
            )
        )
    
    # Authors
    for author in data[input_to_vocab["authors"]]:
        paper.authors.append(
            data_wrapper.Author(
                name = author[input_to_vocab["name"]],
                photo = author[input_to_vocab["photo"]],
                position = author[input_to_vocab["position"]],
                description = author[input_to_vocab["description"]],
                web = author[input_to_vocab["web"]]
            )
        )
    


