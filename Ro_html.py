import json
import properties as p
from bs4 import BeautifulSoup
from shutil import copyfile
from pathlib import Path
import ntpath

class ro_html(object):

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

        # HREF SVG JSONLD            
        jsonld_svg = self.soup.find(id="jsonld_svg")
        jsonld_svg['href'] = ntpath.basename(p.properties["output_jsonld"])

        if p.style == "dark":

            # TODO: Make a function out of this 
            style_component = """
            h1,h1 b{color:#fff!important}
            .w3-light-grey{background-color:#ddd!important;color:#222831!important}
            .w3-green{background-color:#30475e!important}.w3-round{border:5px solid #f05454!important}
            body{background-color:#222831!important;color:#fff!important}
            """
            self.__append_component("style", style_component)
            

    def load_data(self):

        # Iterate attr from data and call correct init function for that attr
        for attr_name in p.data:

            attr_val = getattr(p.data, attr_name)

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

        areas_list = self.__ul_component(areas)

        areas_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Areas</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		{areas_list}
	    </div>"""

        self.__append_component("areas", areas_component)
        self.__sidebar_append("areas", "Areas")


    def init_demo(self, demo):

        demo_list_commponent = self.__ul_component([f"""<a href="{d.link}">{d.link if d.name is None else d.name}</a>: {d.description}""" for d in demo])

        demo_component = f"""<div class="w3-container" id="software" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Demo</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
        {demo_list_commponent}
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
		<h1 class="w3-xxxlarge w3-text-green"><b>Summary</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{summary}</p>
	    </div>"""

        self.__append_component("summary", summary_component)
        self.__sidebar_append("summary", "Summary")
    

    def init_doi_datasets(self, doi_dataset):
        pass
    

    def init_datasets(self, datasets):
 
        datasets_list_commponent = self.__ul_component([f"""<a href="{d.link}">{d.link if d.name is None else d.name}</a>: {d.description}""" for d in datasets])

        doi_datasets = ""
        if p.data.doi_datasets is not None:
            doi_datasets = f"""We used the following datasets for our data, available in Zenodo under DOI: <a href="{p.data.doi_datasets}">{p.data.doi_datasets}</a>"""
        
        datasets_component = f"""<div class="w3-container" id="software" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Datasets</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
        {doi_datasets}
        {datasets_list_commponent}
	    </div>"""

        self.__sidebar_append("datasets", "Datasets")
        self.__append_component("datasets", datasets_component)
    

    def init_software(self, software):

        software_list_commponent = self.__ul_component([f"""<a href="{s.link}">{s.link if s.name is None else s.name}</a>: {s.description}""" for s in software])

        software_component = f"""<div class="w3-container" id="software" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Software</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
        The pointers for the main software used can be found below:
        {software_list_commponent}
	    </div>"""

        self.__sidebar_append("software", "Software")
        self.__append_component("software", software_component)
    

    def init_bibliography(self, bibliography):
 
        bibliography_list = self.__ul_component([b.entry for b in bibliography])

        bibliography_commponent = f"""<div class="w3-container" id="bib" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Bibliography</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
		{bibliography_list}
	    </div>"""

        self.__sidebar_append("bibliography", "Bibliography")
        self.__append_component("bibliography", bibliography_commponent)


    def init_authors(self, authors):
        # create authors
        authors_boxes = self.__create_about_authors(authors)
        authors_commponent = f"""<div class="w3-container" id="authors" style="margin-top:75px">
        <h1 class="w3-xxxlarge w3-text-green"><b>About the authors</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
        {authors_boxes}"""

        self.__sidebar_append("authors", "About the authors")
        self.__append_component("authors", authors_commponent)

        # copy images to output/images directory
        for author in authors:

            src = Path(author.photo)
            dst = Path(p.output_directory + "/" + author.photo)
            
            copyfile(src, dst)


    def __create_about_authors(self, authors):

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

        return html_author


    def create_HTML_file(self):
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


    def __ul_component(self, list):
        ul_list = """<ul>"""
        for li in list:
            ul_list += f"""<li>{li}</li>"""
        ul_list += """</ul>"""
        return ul_list