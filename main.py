# import pyyaml module
import yaml 
from yaml.loader import SafeLoader
# import BeautifulSoup
from bs4 import BeautifulSoup

def append_items_link(category, ul_list):
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

if __name__ == "__main__":

    # open the file and load the file
    with open('properties.yaml') as file:
        properties = yaml.load(file, Loader=SafeLoader)

    with open(properties["input_yaml"]) as file:
        data = yaml.load(file, Loader=SafeLoader)
    
    with open(properties["vocabulary_yaml"]) as file:
        vocabulary = yaml.load(file, Loader=SafeLoader)

    # read and parse the template
    soup = BeautifulSoup(open(properties["template_html"]), 'html.parser')

    # create the title
    soup.find(id = "showcase").h1.string = data[vocabulary["title"]]

    # create the summary
    summary_content = soup.find(id = "summary-content")
    summary_content.string = "Summary: " + data[vocabulary["summary"]]

    # create the datasets
    datasets_list = soup.find(id="datasets-list")
    append_items_link(vocabulary["datasets"], datasets_list)

    # create software
    software_list = soup.find(id="software-list")
    append_items_link(vocabulary["software"], software_list)
        
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

