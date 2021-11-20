```java
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
```

## Install dependencies

* pip install -r requirements.txt

---

## How to use 

Create a yalm file or use one of the templates. Currently ya2ro supports two formats:
- paper
- project

Please find a template for each type under the directory test_files.

The first thing to do is create some input for ya2ro or use one of the yamls under the folder test_files. To create valid yalm you should follow the documentation bellow.   

Once you have a valid yalm (proyect or paper) is time to run ya2ro.

### Comand line arguments
```
usage: ya2ro.py [-h] (-i INPUT | -l LANDING_PAGE) [-o OUTPUT_DIRECTORY] [-p PROPERTIES_FILE]

Human and machine readable input as a yaml file and create RO-Object in jsonld and/or HTML
view.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path of the required yaml input. Follow the documentation or the
                        example given to see the structure of the file.
  -l LANDING_PAGE, --landing_page LANDING_PAGE
                        Path of a previous output folder using the ya2ro tool. This flag will
                        make a landing page to make all the resources accesible.
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Output diretory.
  -p PROPERTIES_FILE, --properties_file PROPERTIES_FILE
                        Properties file name.
```

### Create machine and human readable content

It is possible to process batches of yalms at the same time, to do that just specify as input a folder with all the yalms inside.

##### Simple execution:

`python3 ya2ro.py -i test_files`   
`python3 ya2ro.py -i test_files/project_yemplate.yaml`   

##### With optional arguments:

`python3 ya2ro.py -input test_files --output_directory out --properties_file custom_properties.yaml`   
`python3 ya2ro.py -i test_files -o out -p custom_properties.yaml`

### Create landing page

ya2ro offers the option to create a landing page where all the resources produced are easilly accesible. Just indicate the folder where this resources are, for example:

`python3 ya2ro.py -l output`

---


## Fields supported

### Paper   
Documentation for all supported fields for type paper.   

`type:`This field is required and is used to indicate the type of the work.
```yaml
type: "paper"
```

`title:`Title of the paper.
```yaml
title: "Paper - Template"
```

`summary:`A brief summary of the paper, also known as an abstract.
```yaml
summary: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed finibus odio egestas neque porttitor sollicitudin. Sed fermentum placerat nisi quis congue."
```

`datasets:` All the datasets used and created during the paper. This tool supports to define each dataset manually specifying all fields or to use a DOI and ya2ro will try to automatically fetch the data.
```yaml
datasets:
  - 
    doi_dataset: www.doiDB1.com
  - 
    link: www.D1.com 
    name: "Dataset 1"
    description: "Description dataset 1"
```

`software:` All the relevant software used and created for the paper. If a GitHub Repo is provided ya2ro will use SOMEF to automatically fetch relevant data.
```yaml
software:
  -
    link: https://github.com/KnowledgeCaptureAndDiscovery/somef/
  - 
    link: http://software_1.com 
    name: "Software 1"
    description: "Description software 1"
    license: "MIT-License"
```

`bibliography:`In this field is where the bibliography can be added.
```yaml
bibliography:
  - "Bibliography entry 1"
  - "Bibliography entry 2"
  - "Bibliography entry 3"
```
`authors:`In this field is where credit to the creators, collaborators, authors, etc is given. If an ORCID is privided, ya2ro will fetch relevant data automatically. If a photo is not provided, a default one will be used.
```yaml
authors:
    -
      orcid: https://orcid.org/0000-0003-0454-7145
      role: "Coordinator"
    -
      name: "Author"
      position: "Author's position"
      description: "Author's description"
      web: https://author-web.com/
      photo: "author_photo.jpg"
```
---

### Project   
Documentation for all supported fields for type project.   

`type:`This field is required and is used to indicate the type of the work.
```yaml
type: "prpject"
```

`title:`Title of the project.
```yaml
title: "Project - Template"
```
`goal:`In this field you should inlcude the goal for the project.
```yaml
goal: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed finibus odio egestas neque porttitor sollicitudin."
```
`social_motivation:`In this field you should include why this project will help in a social way.
```yaml
social_motivation: "Suspendisse est justo, finibus a nisi eget, condimentum imperdiet mi. Mauris sagittis diam mi, sit amet blandit ipsum semper sed."
```
`sketch:`Path to an image where a visual description/workflow is shown.
```yaml
sketch: "images/sketch_ya2ro.jpg"
```
`areas:`All the areas involucrated inside this project.
```yaml
areas: 
  - "Area 1: Some description."
  - "Area 2: Some description."
```

`activities:`All the idividual subtasks of the project.
```yaml
activities:
  - "Subtask 1: Some description."
  - "Subtask 2: Some description."
```

`demo:`Link or links to demos of the project.
```yaml
demo: 
  -
    link: http://demo.com
    description: "This is a description for a demo."
  -
    name: "Demo name"
    link: http://demo.com
    description: "This is a description for a demo with name."
```

`datasets:` All the datasets used and created during the project. This tool supports to define each dataset manually specifiying all fields or to use a DOI and ya2ro will try to automatically fetch the data.
```yaml
datasets:
  - 
    doi_dataset: www.doiDB1.com
  - 
    link: www.D1.com 
    name: "Dataset 1"
    description: "Description dataset 1"
```
`software:` All the relevant software used and created for the paper. If a GitHub Repo is provided, ya2ro will use SOMEF to automatically fetch relevant data.
```yaml
software:
  -
    link: https://github.com/KnowledgeCaptureAndDiscovery/somef/
  - 
    link: http://software_1.com 
    name: "Software 1"
    description: "Description software 1"
    license: "MIT-License"
```

`bibliography:`In this field is where the bibliography can be added.
```yaml
bibliography:
  - "Bibliography entry 1"
  - "Bibliography entry 2"
  - "Bibliography entry 3"
```

`authors:`In this field is where credit to the creators, collaborators, authors, etc is given. If an ORCID is privided ya2ro will fetch relevant data automatically. If a photo is not provided, a default one will be used.
```yaml
participatns:
    -
      orcid: https://orcid.org/0000-0003-0454-7145
      role: "Coordinator"
    -
      name: "Author"
      position: "Author's position"
      description: "Author's description"
      web: https://author-web.com/
      photo: "author_photo.jpg"
```
`contact:`In this field you can add some contact information.
```yaml
contact:
  email: contact@projectmail.com
  phone: +34 999 999 999
```



