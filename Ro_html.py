# import BeautifulSoup
from Orcid_req import Orcid_req
import Properties
from bs4 import BeautifulSoup
from shutil import copyfile
from pathlib import Path


class Ro_html(object):

    # The class "constructor" - It's actually an initializer 
    def __init__(self):

        # read and parse the template
        self.soup = BeautifulSoup(open(Properties.properties["template_html"]), 'html.parser')

        # modify web title metadata
        self.soup.find('title').string = Properties.data[Properties.input_to_vocab["title"]]

        # create the title
        self.soup.find(id = "showcase").h1.string = Properties.data[Properties.input_to_vocab["title"]]

        # create the summary
        summary_content = self.soup.find(id = "summary-content")
        summary_content.string = "Summary: " + Properties.data[Properties.input_to_vocab["summary"]]

        # create the datasets
            # Insert DOI link
        doi_link = Properties.data[Properties.input_to_vocab["datasets"]][Properties.input_to_vocab["doi"]]
        dataset_doi_string = f"""We used the following datasets for our paper, available in Zenodo under DOI: <a href="{doi_link}">{doi_link}</a>"""
        doi_html = BeautifulSoup(dataset_doi_string, 'html.parser')
        datasets = self.soup.find(id="datasets-doi")
        datasets.append(doi_html)

            # Insert list of datasets
        datasets_list = self.soup.find(id="datasets-list")
        self.__append_items_link(
            Properties.data[Properties.input_to_vocab["datasets"]][Properties.input_to_vocab["datasets_links"]], 
            datasets_list
            )

        # create software
        software_list = self.soup.find(id="software-list")
        self.__append_items_link(
            Properties.data[Properties.input_to_vocab["software"]], 
            software_list
            )
            
        # create bibliography
        bibliography_list = self.soup.find(id="bibliography-list")

        for entry in Properties.data[Properties.input_to_vocab["bibliography"]]:
            li_new_tag = self.soup.new_tag('li')
            li_new_tag.string = entry
            bibliography_list.append(li_new_tag)

        # create authors
        about_authors = self.soup.find(id="about_authors")
        self.__create_about_authors(about_authors)

    def createHTML_file(self):
        """Dupms index.html and dependencies into specified folder. Including .htacces"""
        # dump changes into index.html
        with open(Properties.properties["output_html"], "w+") as file:
            file.write(str(self.soup))

        # copy images to output/images directory

        for author in Properties.data["authors"]:

            src = Path(author[Properties.input_to_vocab["photo"]])
            dst = Path(Properties.output_directory + "/" + author[Properties.input_to_vocab["photo"]])
            
            copyfile(src, dst)

        # Copy .htaccess to output folder
        copyfile(Properties.properties["htaccess"],Path(Properties.output_directory+"/.htaccess"))


    def __append_items_link(self, list, ul_list):
        for entry in list:
            li_new_tag = self.soup.new_tag('li')
            a_new_tag = self.soup.new_tag('a')
            a_new_tag['href'] = entry[Properties.input_to_vocab["link"]]
            a_new_tag.string = entry[Properties.input_to_vocab["name"]]
            li_new_tag.append(a_new_tag)
            li_new_tag.a.insert_after(": " + entry[Properties.input_to_vocab["description"]])
            ul_list.append(li_new_tag)
    
    def __create_about_authors(self, about_authors):
        num_authors = 0
        html_author = ""

        for author in Properties.data[Properties.input_to_vocab["authors"]]:

            num_authors += 1

            if((num_authors-1) %3 == 0):
                html_author += """<div class="w3-row-padding">"""

            if Properties.input_to_vocab["orcid"] in author:
                orcid = Orcid_req(author[Properties.input_to_vocab["orcid"]])
                name = orcid.get_full_name()
                position = "\n".join(orcid.get_affiliation())
                web = orcid.get_webs()[-1]
            else:
                name = author[Properties.input_to_vocab["name"]]
                position = author[Properties.input_to_vocab["position"]]
                web = author[Properties.input_to_vocab["web"]]

            photo_path = author[Properties.input_to_vocab["photo"]]
            description = author[Properties.input_to_vocab["description"]]

            html_author += f"""       <div class="w3-col m4 w3-margin-bottom">
                <div class="w3-light-grey">
                <img src="{photo_path}" alt="{name}" style="width:90%;padding-top: 10px;">
                <div class="w3-container">
                    <h3>{name}</h3> 
                    <p class="w3-opacity"> {position}</p>
                    <a href="{web}">{web}</a>
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


