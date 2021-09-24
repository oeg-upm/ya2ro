# import pyyaml module
import yaml 
from yaml.loader import SafeLoader
# import BeautifulSoup
from bs4 import BeautifulSoup
# import json lib
import json


def append_items_link(soup, category, ul_list):
    for entry in data[category]:
        li_new_tag = soup.new_tag('li')
        a_new_tag = soup.new_tag('a')
        a_new_tag['href'] = entry[vocabulary["link"]]
        a_new_tag.string = entry[vocabulary["name"]]
        li_new_tag.append(a_new_tag)
        li_new_tag.a.insert_after(": " + entry[vocabulary["description"]])
        ul_list.append(li_new_tag)

def create_about_authors(about_authors):
    num_authors = 0
    html_author = ""

    for author in data[vocabulary["authors"]]:

        num_authors += 1

        if((num_authors-1) %3 == 0):
            html_author += """<div class="w3-row-padding">"""

        name = author[vocabulary["name"]]
        photo_path = author[vocabulary["photo"]]
        position = author[vocabulary["position"]]
        description = author[vocabulary["description"]]

        html_author += f"""       <div class="w3-col m4 w3-margin-bottom">
            <div class="w3-light-grey">
            <img src="{photo_path}" alt="{name}" style="width:100px;padding-top: 10px;">
            <div class="w3-container">
                <h3>{name}</h3> 
                <p class="w3-opacity"> {position}</p>
                <p>{description}</p>
            </div>
            </div>
        </div> """ 

        if(num_authors !=0 and num_authors %3 == 0):
            html_author += "</div>"
        
    if(not(num_authors !=0 and num_authors %3 == 0)):
        html_author += "</div>"

    author_bs = BeautifulSoup(html_author, 'html.parser')
    about_authors.append(author_bs)

def create_html_from_yalm():
    # read and parse the template
    soup = BeautifulSoup(open(properties["template_html"]), 'html.parser')

    # create the title
    soup.find(id = "showcase").h1.string = data[vocabulary["title"]]

    # create the summary
    summary_content = soup.find(id = "summary-content")
    summary_content.string = "Summary: " + data[vocabulary["summary"]]

    # create the datasets
    datasets_list = soup.find(id="datasets-list")
    append_items_link(soup, vocabulary["datasets"], datasets_list)

    # create software
    software_list = soup.find(id="software-list")
    append_items_link(soup, vocabulary["software"], software_list)
        
    # create bibliography
    bibliography_list = soup.find(id="bibliography-list")

    for entry in data[vocabulary["bibliography"]]:
        li_new_tag = soup.new_tag('li')
        li_new_tag.string = entry
        bibliography_list.append(li_new_tag)

    # create authors
    about_authors = soup.find(id="about_authors")
    create_about_authors(about_authors)

    # dump changes into index.html
    with open(properties["output_html"], "w") as file:
        file.write(str(soup))

def graph_add_authors(authors, graph):

    graph[1]["author"] = []

    for author in authors:

        graph[1]["author"].append(author[vocabulary["name"]])

        graph.append({
        "@id": "#"+author[vocabulary["name"]],
        "@type": "Person",
        "name": author[vocabulary["name"]],
        "position": author[vocabulary["position"]],
        "description": author[vocabulary["description"]]
      })

def graph_add_softwares(softwares, graph):

    software_node = {
        "@id": "#softwares",
        "@type": "SoftwareApplication",
        "hasPart": []
      }
    
    for software in softwares:

        software_node["hasPart"].append(software[vocabulary["name"]])

        graph.append({
        "@id": software[vocabulary["name"]],
        "installUrl": software[vocabulary["link"]],
        "@type": "SoftwareApplication",
        "description": software[vocabulary["description"]]
      })

    graph.insert(-len(softwares),software_node)

def graph_add_datasets(datasets, graph):

    dataset_node = {
        "@id": "#datasets",
        "@type": "Dataset",
        "hasPart": []
      }
    
    for dataset in datasets:
        dataset_node["hasPart"].append(dataset[vocabulary["name"]])

        graph.append({
            "@id": dataset[vocabulary["name"]],
            "@type": "Dataset",
            "name": dataset[vocabulary["name"]],
            "description": dataset[vocabulary["description"]],
            "distribution": {"@id": dataset[vocabulary["link"]]}
        })

        graph.append({
            "@id": dataset[vocabulary["link"]],
            "@type": "DataDownload",
            "encodingFormat": "application/zip"
        })

    graph.insert(-len(datasets)*2, dataset_node)

def create_jsondl_from_yalm():
    
    jsonld = {}
    jsonld["@context"] = "https://w3id.org/ro/crate/1.1/context"
    graph = [
        {
            "@type": "CreativeWork",
            "@id": "ro-crate-metadata.json",
            "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
            "about": {"@id": "./"},
            "description": "RO-Crate Metadata File Descriptor (this file)"
        },
        {
          "@id": "./",
          "@type": "Paper",
          "name": data[vocabulary["title"]],
          "description": data[vocabulary["summary"]],
          "author": [],
          "hasPart": [
            {"@id": "#softwares"},
            {"@id": "#datasets"}
          ]
      }
    ]

    graph_add_authors(data[vocabulary["authors"]], graph)
    graph_add_softwares(data[vocabulary["software"]], graph)
    graph_add_datasets(data[vocabulary["datasets"]], graph)

    jsonld["@graph"] = graph

    # dump changes into jsondl
    with open(properties["output_jsondl"], "w") as file:
        file.write(json.dumps(jsonld, indent=4, sort_keys=True))

if __name__ == "__main__":

    # open the file and load the file
    with open('properties.yaml') as file:
        properties = yaml.load(file, Loader=SafeLoader)

    with open(properties["input_yaml"]) as file:
        data = yaml.load(file, Loader=SafeLoader)
    
    with open(properties["vocabulary_yaml"]) as file:
        vocabulary = yaml.load(file, Loader=SafeLoader)

    create_html_from_yalm()
    create_jsondl_from_yalm()

