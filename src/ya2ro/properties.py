import yaml 
from yaml.loader import SafeLoader
from pathlib import Path
import os

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

    configure_somef(properties_file)

    print(f"{style} theme selected.")
    print("Properties initialized...")

def configure_somef(properties_file):

    if os.path.isfile(Path(base_dir)/'resources'/'is_somef_configured'):
        return

    from somef import configuration
    print("Running SOMEF initial configuration:")
    token = _safe('GITHUB_PERSONAL_ACCESS_TOKEN', properties)
    if token:
        configuration.configure(authorization=token)
        with open(Path(base_dir)/'resources'/'is_somef_configured', 'w+') as f:
            f.write('Yes :D')
    else:
        print(
            f"""
WARNING: GITHUB_PERSONAL_ACCESS_TOKEN is not configured. Please add your personal token in ya2ro configuration file.
        --> {Path(base_dir, properties_file)} <--

        ADD a line like the following:
        GITHUB_PERSONAL_ACCESS_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        ya2ro will continue working, but is highly recommended to apply this setting.
            """
        )


def _safe(key, dic):
    """Safe call to a dictionary. Returns value or None if key or dictionary does not exist"""
    return dic[key] if dic and key in dic else None
