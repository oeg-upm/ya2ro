# EELISA-research-object

## Install dependencies

* pip install -r requirements.txt

## How to use 

Insert data into the example template.yaml file or create a new one, keeping the same structure.
For further customization use custom properties file.

---

```
                        ad888888b,                         
                       d8"     "88                         
                               a8P                         
8b       d8 ,adPPYYba,      ,d8P"  8b,dPPYba,  ,adPPYba,   
`8b     d8' ""     `Y8    a8P"     88P'   "Y8 a8"     "8a  
 `8b   d8'  ,adPPPPP88  a8P'       88         8b       d8  
  `8b,d8'   88,    ,88 d8"         88         "8a,   ,a8"  
    Y88'    `"8bbdP"Y8 88888888888 88          `"YbbdP"'   
    d8'                                                    
   d8' 
_________________________________________________________
    
usage: ya2ro.py [-h] (-i INPUT | -l LANDING_PAGE) [-o OUTPUT_DIRECTORY] [-p PROPERTIES_FILE]

Human and machine readeable input as a yalm file and create RO-Object in jsonld and/or HTML view.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path of the required yalm input. Follow the documentation or the example given to see the
                        structure of the file.
  -l LANDING_PAGE, --landing_page LANDING_PAGE
                        Path of a previous output folder using the ya2ro tool. This flag will make a landing page
                        to make all the resources accesible.
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Output diretory.
  -p PROPERTIES_FILE, --properties_file PROPERTIES_FILE
                        Properties file name.
```

## Example of use

### Create individual pages

Simple execution:

`python3 ya2ro.py -i test_files`   
`python3 ya2ro.py -i test_files/project_yemplate.yaml`   


With optional arguments:

`python3 ya2ro.py -input test_files --output_directory out --properties_file custom_properties.yaml`   
`python3 ya2ro.py -i test_files -o out -p custom_properties.yaml`

### Create landing page

`python3 ya2ro.py -l output`


