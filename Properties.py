import yaml 
from yaml.loader import SafeLoader
from pathlib import Path


def init(properties_file, output_directory_param):
    global output_directory, input_to_vocab, properties, style
    
    # Make visible output directoty to all modules
    output_directory = output_directory_param

    # Create paths for output files
    with open(Path(properties_file)) as file:
        properties = yaml.load(file, Loader=SafeLoader)
    
    # Load vocab used in the input.yalm
    with open(Path(properties["input_to_vocab_yaml"])) as file:
        input_to_vocab = yaml.load(file, Loader=SafeLoader)
    
    # Style selector
    style = _safe(input_to_vocab["style"], properties)
    style = style if style else "default"


def _safe(key, dic):
    """Safe call to a dictionary. Returns value or None if key or dictionary does not exist"""
    if dic is not None and key in dic:
        return dic[key]
    else:
        return None