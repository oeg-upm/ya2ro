# ya2ro

[![DOI](https://zenodo.org/badge/407588137.svg)](https://zenodo.org/badge/latestdoi/407588137) [![Project Status: Active: The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Example

Ya2ro generates Research Objects (ROs) like the following: [https://w3id.org/dgarijo/ro/sepln2022](https://w3id.org/dgarijo/ro/sepln2022). Given a few ROs, `ya2ro` can also create a landing page:
<https://oeg-upm.github.io/ya2ro/output/landing_page.html>

## Requirements
The latest version of ya2ro works in Python 3.10.

## Installation

To run ya2ro, please follow the next steps:

### Install from PyPI

```text
pip install ya2ro
```

### Install from GitHub

```text
git clone https://github.com/oeg-upm/ya2ro
cd ya2ro
pip install -e .
```

### Installing through Docker

We provide a Dockerfile with ya2ro already installed. To run through Docker, you may build the Dockerfile provided in the repository by running:

```bash
docker build -t ya2ro .
```

Then, to run your image just type:

```bash
docker run -it ya2ro /bin/bash
```

And you will be ready to use ya2ro (see section below). If you want to have access to the results we recommend [mounting a volume](https://docs.docker.com/storage/volumes/). For example, the following command will mount the current directory as the `out` folder in the Docker image:

```bash
docker run -it --rm -v $PWD/:/out ya2ro /bin/bash
```

If you move any files produced by ya2ro into `/out`, then you will be able to see them in your current directory.

## Usage

### Configure

Before running ya2ro, you must configure it appropriately. Please add your GitHub personal token in ya2ro properties file. This needed if you want `ya2ro` to extract your software metadata automatically. The file can be found at:

`--> ~/ya2ro/src/ya2ro/resources/properties.yaml <--`

Add a line like the following:

```yaml
# Add here your GitHub personal access token
GITHUB_PERSONAL_ACCESS_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 
```

ya2ro will work if this is not configured, but is highly recommended to apply this setting, as the GitHub API has restricted access.

### Test ya2ro installation

```bash
ya2ro --help
```

If everything goes fine, you should see:

```text
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

usage: ya2ro [-h] (-i YAML_PATH | -l YA2RO_PREV_OUTPUT) [-o OUTPUT_DIR] [-p PROPERTIES_FILE] [-ns]

Human and machine readable input as a yaml file and create RO-Object in jsonld and/or HTML view. Run 'ya2ro -configure GITHUB_PERSONAL_ACCESS_TOKEN' this the first time to configure ya2ro
properly

options:
  -h, --help            show this help message and exit
  -i YAML_PATH, --input YAML_PATH
                        Path of the required yaml input. Follow the documentation or the example given to see the structure of the file.
  -l YA2RO_PREV_OUTPUT, --landing_page YA2RO_PREV_OUTPUT
                        Path of a previous output folder using the ya2ro tool. This flag will make a landing page to make all the resources accessible.
  -o OUTPUT_DIR, --output_directory OUTPUT_DIR
                        Output directory.
  -p PROPERTIES_FILE, --properties_file PROPERTIES_FILE
                        Properties file name.
  -ns, --no_somef       Disable SOMEF for a faster execution (software cards will not work).

```

---

### How to use  

The first thing to do is create some input for ya2ro. To create valid a yaml you should follow the documentation bellow.

Create a yaml from scratch or use one of the supplied templates. Currently ya2ro supports two formats:

* paper
* project

Please find a template for each type under the directory templates.
Once you have a valid yaml (project or paper) is time to run ya2ro.

#### Create machine and human readable content

It is possible to process batches of yamls at the same time, to do that just specify as input a folder with all the yamls inside.

##### Simple execution

`ya2ro -i templates`  

`ya2ro -i templates/project_template.yaml`

##### With optional arguments

`ya2ro -input templates --output_directory out --properties_file custom_properties.yaml`  

`ya2ro -i templates -o out -p custom_properties.yaml`

##### Faster execution?

Use the flag --no_somef or -ns for disabling SOMEF which is the most time consuming process.

`ya2ro -i templates -ns`

WARNING: Software cards will no longer work on github links. Therefore you will need to manually insert the software data in the yaml file.

#### Create landing page

ya2ro offers the option to create a landing page where all the resources produced are easily accessible. Just indicate the folder where this resources are, for example:

`ya2ro -l output`

## Documentation
Please have a look at our [documentation](Documentation.md) to know which metadata fields are supported by `ya2ro`.
