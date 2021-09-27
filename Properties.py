# import pyyaml module
import yaml 
from yaml.loader import SafeLoader
    
with open('properties.yaml') as file:
    properties = yaml.load(file, Loader=SafeLoader)

with open(properties["input_yaml"]) as file:
    data = yaml.load(file, Loader=SafeLoader)

with open(properties["input_to_vocab_yaml"]) as file:
    input_to_vocab = yaml.load(file, Loader=SafeLoader)

