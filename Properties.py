import yaml 
from yaml.loader import SafeLoader
from pathlib import Path
import os


def init(properties_file, input_yalm, output_directory):
    global properties, data, input_to_vocab

    with open(Path(properties_file)) as file:
        properties = yaml.load(file, Loader=SafeLoader)
    properties["output_html"] = Path(output_directory +"/"+ properties["output_html"])
    properties["output_jsonld"] = Path(output_directory +"/"+ properties["output_jsonld"])

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


    with open(Path(input_yalm)) as file:
        data = yaml.load(file, Loader=SafeLoader)


    with open(Path(properties["input_to_vocab_yaml"])) as file:
        input_to_vocab = yaml.load(file, Loader=SafeLoader)

