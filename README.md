# EELISA-research-object

## Install dependencies

* pip install -r requirements.txt 

## How to use 

Insert data into the example input.yaml file or create a new one, keeping the same structure.
Run the script as follows:

---

```
Usage: main.py [-h] -i INPUT [-o OUTPUT_DIRECTORY] [-p PROPERTIES_FILE]

Human and machine readeable input as a yalm file and create RO-Object in jsonld and/or HTML view.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path of the required yalm input. Follow the documentation or the example given to see the structure of the file.
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Output diretory.
  -p PROPERTIES_FILE, --properties_file PROPERTIES_FILE
                        Properties file name.
```

## Example of use

Simple execution:

`python3 ya2ro.py -i input.yaml`

With optional arguments:

`python3 ya2ro.py -input input.yaml --output_directory out --properties_file prop.yaml`   
`python3 ya2ro.py -i input.yaml -o out -p prop.yaml`
