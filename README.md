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
usage: main.py [-h] [--output_directory OUTPUT_DIRECTORY] [--properties_file PROPERTIES_FILE] input_yalm

Positional arguments:
  input_yalm            Path of required yalm input, follow the documentation or the example given to see the structure of the
                        file.

Optional arguments:
  -h, --help            show this help message and exit
  --output_directory OUTPUT_DIRECTORY
                        Output diretory.
  --properties_file PROPERTIES_FILE
                        Properties file name.
```

## Example of use

Simple exeution:

`python3 main.py input.yaml`

With optional arguments:

`python3 main.py input.yaml --output_directory out --properties_file prop.yaml`