# import pyyaml module
import yaml 
from yaml.loader import SafeLoader
# import BeautifulSoup
from bs4 import BeautifulSoup
# import RegEx
import re

def append_items_link(category, ul_list):
    for entry in data[category]:
        li_new_tag = soup.new_tag('li')
        a_new_tag = soup.new_tag('a')

        link_and_description = entry.split(';', 2) 
        # 0: link, 1: link name, 2: description
        a_new_tag['href'] = link_and_description[0]
        a_new_tag.string = link_and_description[1]
        li_new_tag.append(a_new_tag)
        li_new_tag.a.insert_after(": " + link_and_description[2])
        ul_list.append(li_new_tag)

def create_about_authors(about_authors):
    num_authors = 0
    html_author = ""

    for author in data["authors"]:

        num_authors += 1

        if((num_authors-1) %3 == 0):
            html_author += """<div class="w3-row-padding">"""

        name = author["name"]
        photo_path = author["photo_path"]
        position = author["position"]
        description = author["description"]

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
    with open('input.yaml') as file:
        data = yaml.load(file, Loader=SafeLoader)

    # read and parse the template
    soup = BeautifulSoup(open('template.html'), 'html.parser')

    # create the title
    soup.find(id = "showcase").h1.string = data["title"]

    # create the summary
    summary_content = soup.find(id = "summary-content")
    summary_content.string = "Summary: " + data["summary"]

    # create the datasets
    datasets_list = soup.find(id="datasets-list")
    append_items_link("datasets", datasets_list)

    # create software
    software_list = soup.find(id="software-list")
    append_items_link("software", software_list)
        
    # create bibliography
    bibliography_list = soup.find(id="bibliography-list")

    for entry in data["bibliography"]:
        li_new_tag = soup.new_tag('li')
        li_new_tag.string = entry
        bibliography_list.append(li_new_tag)

    # create authors
    about_authors = soup.find(id="about_authors")
    create_about_authors(about_authors)

    # dump changes into index.html
    with open("index.html", "w") as file:
        file.write(str(soup))

