import Properties as p
from bs4 import BeautifulSoup
from shutil import copyfile
from pathlib import Path


class Ro_html(object):

    def __init__(self):

        # read and parse the template
        self.soup = BeautifulSoup(open(p.properties["template_html"]), 'html.parser')

        self.func_attr_init = {

            "title": self.init_title,
            "summary": self.init_summary,
            "doi_datasets": self.init_doi_datasets,
            "datasets": self.init_datasets,
            "software": self.init_software,
            "bibliography": self.init_bibliography,
            "authors": self.init_authors,
            "goal": self.init_goal,
            "social_motivation": self.init_social_motivation,
            "sketch": self.init_sketch,
            "areas": self.init_areas,
            "demo": self.init_demo

        }

    def load_data(self):

        # Iterate attr from data and call correct init function for that attr
        for attr_name in p.data:

            attr_val = getattr(p.data, attr_name)
            #print("Attr name: ", attr_name)
            #print("Attr val: ", attr_val)

            if attr_val and attr_name in self.func_attr_init:
                self.func_attr_init[attr_name](attr_val)
    
    def init_social_motivation(self, social_motivation):

        social_motivation_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Social Motivation</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{social_motivation}</p>
	    </div>"""

        self.__append_component("social_motivation", social_motivation_component)
        self.__sidebar_append("social_motivation", "Social motivation")
    
    def init_sketch(self, sketch):
        
        sketch_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Sketch</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<img src="{sketch}" alt="Sketch of the project">
	    </div>"""
        self.__append_component("sketch", sketch_component)
        self.__sidebar_append("sketch", "Sketch")


        # copy image to output/images directory
        src = Path(sketch)
        dst = Path(p.output_directory + "/" + sketch)
        copyfile(src, dst)
    
    def init_areas(self, areas):

        areas_list = self.__make_html_ul_component(areas)

        areas_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Areas</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		{areas_list}
	    </div>"""
        self.__append_component("areas", areas_component)
        self.__sidebar_append("areas", "Areas")
    
    def init_demo(self, demo):
        
        demo_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Demo</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p><a href="{demo}">{demo}</a></p>
	    </div>"""

        self.__append_component("demo", demo_component)
        self.__sidebar_append("demo", "Demo")


    def init_goal(self, goal):

        goal_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Goal</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{goal}</p>
	    </div>"""

        self.__append_component("goal", goal_component)
        self.__sidebar_append("goal", "Goal")
 

    def init_title(self, title):
        # modify web title metadata
        self.soup.find('title').string = title
        # create the title
        self.soup.find(id = "showcase").h1.string = title
    
    def init_summary(self, summary):

        summary_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Goal</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{summary}</p>
	    </div>"""

        self.__append_component("summary", summary_component)
        self.__sidebar_append("summary", "Summary")
    
    def init_doi_datasets(self, doi_dataset):
        # Insert DOI link
        doi_link = doi_dataset
        dataset_doi_string = f"""We used the following datasets for our data, available in Zenodo under DOI: <a href="{doi_link}">{doi_link}</a>"""
        doi_html = BeautifulSoup(dataset_doi_string, 'html.parser')
        datasets = self.soup.find(id="datasets-doi")
        datasets.append(doi_html)
    
    def init_datasets(self, datasets):
        # Insert list of datasets
        datasets_list = self.soup.find(id="datasets-list")
        self.__append_items_link(datasets, datasets_list)
        self.__sidebar_append("datasets", "Datasets")
    
    def init_software(self, software):
        # create software
        software_list = self.soup.find(id="software-list")
        self.__append_items_link(software, software_list)
        self.__sidebar_append("software", "Software")
    
    def init_bibliography(self, bibliography):
        # create bibliography
        bibliography_list = self.soup.find(id="bibliography-list")
        for entry in bibliography:
            li_new_tag = self.soup.new_tag('li')
            li_new_tag.string = entry.entry
            bibliography_list.append(li_new_tag)
        self.__sidebar_append("bibliography", "Bibliography")

    def init_authors(self, authors):
        # create authors
        about_authors = self.soup.find(id="about_authors")
        self.__create_about_authors(authors, about_authors)
        self.__sidebar_append("authors", "About the authors")

        # copy images to output/images directory
        for author in authors:

            src = Path(author.photo)
            dst = Path(p.output_directory + "/" + author.photo)
            
            copyfile(src, dst)
    

    def __append_items_link(self, list, ul_list):
        for entry in list:
            li_new_tag = self.soup.new_tag('li')
            a_new_tag = self.soup.new_tag('a')
            a_new_tag['href'] = entry.link
            a_new_tag.string = entry.name
            li_new_tag.append(a_new_tag)
            li_new_tag.a.insert_after(": " + entry.description)
            ul_list.append(li_new_tag)
    
    def __create_about_authors(self, authors, about_authors):
        num_authors = 0
        html_author = ""

        for author in authors:

            num_authors += 1

            if((num_authors-1) %3 == 0):
                html_author += """<div class="w3-row-padding">"""

            html_author += f"""
            <div class="w3-col m4 w3-margin-bottom">
                <div class="w3-light-grey">
                <img src="{author.photo}" alt="{author.name}" style="width:90%;padding-top: 10px;">
                <div class="w3-container">
                    <h3><a href="{author.orcid if author.orcid is not None else author.web}">{author.name}</a></h3>
                    <p class="w3-opacity"> {author.position}</p>
                    <a href="{author.web}">{author.web}</a>
                    <p>{author.description}</p>
                    
                </div>
                </div>
            </div> 
            """

            if(num_authors !=0 and num_authors %3 == 0):
                html_author += "</div>"
            
        if(not(num_authors !=0 and num_authors %3 == 0)):
            html_author += "</div>"

        author_bs = BeautifulSoup(html_author, 'html.parser')
        about_authors.append(author_bs)

    def createHTML_file(self):
        """Dupms index.html and dependencies into specified folder."""
        # dump changes into index.html
        with open(p.properties["output_html"], "w+") as file:
            file.write(str(self.soup))
        
        print(f"HTML website file created at {p.properties['output_html']}")   

    def __append_component(self, location_id, str_component):
        loc = self.soup.find(id=location_id)
        html_component = BeautifulSoup(str_component, 'html.parser')
        loc.append(html_component)
    
    def __sidebar_append(self, location_id, item_name):
        item_component = f"""<a href="#{location_id}" onclick="w3_close()" class="w3-bar-item w3-button w3-hover-white">{item_name}</a>"""
        self.__append_component("sidebar", item_component)

    def __make_html_ul_component(self, list):
        ul_component = """<ul>"""
        for li in list:
            ul_component += f"""<li>{li}</li>"""
        ul_component += """</ul>"""
        return ul_component