import yaml 
from yaml.loader import SafeLoader
from pathlib import Path


def init(properties_file, output_directory_param, n_somef):
    global output_directory, input_to_vocab, properties, style, base_dir, no_somef

    # Disable somef flag
    no_somef = n_somef
    
    # Project base path
    base_dir = str(Path(__file__).parent.resolve())
    
    # Make visible output directoty to all modules
    output_directory = output_directory_param

    # Create paths for output files
    with open(Path(base_dir, properties_file)) as file:
        properties = yaml.load(file, Loader=SafeLoader)
    
    # Load vocab used in the input.yaml
    with open(Path(base_dir, properties["input_to_vocab_yaml"])) as file:
        input_to_vocab = yaml.load(file, Loader=SafeLoader)
    
    # Style selector
    style = _safe(input_to_vocab["style"], properties)
    style = style if style else "default"

    print(f"{style} theme selected.")
    print("Properties initialized...")


def _safe(key, dic):
    """Safe call to a dictionary. Returns value or None if key or dictionary does not exist"""
    if dic is not None and key in dic:
        return dic[key]
    else:
        return None
