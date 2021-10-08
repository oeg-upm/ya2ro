# EELISA-research-object

## Install dependencies

* pip install pyyaml
* pip install bs4
* pip install json 

## How to use 

Insert data into the example input.yaml file or create a new one, keeping the same structure.
Run the script as follows:

---

```
Usage: main.py [-h] -i INPUT_FILE [--output_directory OUTPUT_DIRECTORY] [--properties_file PROPERTIES_FILE]

Human and machine readeable input as a yalm file and create RO-Object in jsonld and/or HTML view.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE         Path of the required yalm input. Follow the documentation or the example given to see the structure of the file.
  --output_directory OUTPUT_DIRECTORY
                        Output diretory.
  --properties_file PROPERTIES_FILE
                        Properties file name.
```

## Example of use

Simple execution:

`python3 main.py -i input.yaml`

With optional arguments:

`python3 main.py -i input.yaml --output_directory out --properties_file prop.yaml`