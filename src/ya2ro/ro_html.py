from . import properties as p
from bs4 import BeautifulSoup
from shutil import copyfile
from pathlib import Path
import ntpath
from . import hilite_me
from scc.commands.portal.card import html_view as card_html_view
import os
import re

class ro_html(object):

    def __init__(self):

        # read and parse the templates
        self.soup = BeautifulSoup(open(Path(p.base_dir,p.properties["template_html"])), 'html.parser')
        self.soup_help = BeautifulSoup(open(Path(p.base_dir,p.properties["template_help"])), 'html.parser')

        self.func_attr_init = {

            "title": self.init_title,
            "summary": self.init_summary,
            "datasets": self.init_datasets,
            "software": self.init_software,
            "bibliography": self.init_bibliography,
            "authors": self.init_authors,
            "goal": self.init_goal,
            "social_motivation": self.init_social_motivation,
            "sketch": self.init_sketch,
            "areas": self.init_areas,
            "activities": self.init_activities,
            "demo": self.init_demo,
            "requirements": self.init_requirements_recognition,
            "contact": self.init_contact,
            "bib": self.init_bib

        }


    def load_data(self, data):

        self.data = data

        # HREF SVG JSONLD            
        jsonld_svg = self.soup.find(id="jsonld_svg")
        jsonld_svg['href'] = ntpath.basename(self.data.output_jsonld)

        # HREF Help button
        help_button = self.soup.find(id="help-button")
        help_button['href'] = ntpath.basename(self.data.output_html_help)

        # HREF Back button from help
        back_button = self.soup_help.find(id="back-button")
        back_button['href'] = ntpath.basename(self.data.output_html)

        # Iterate attr from data and call correct init function for that attr
        for attr_name in self.data:

            attr_val = getattr(self.data, attr_name)

            if attr_val and attr_name in self.func_attr_init:
                self.func_attr_init[attr_name](attr_val)

        self.init_styles()
        self.init_help_page()
    
    def init_bib(self, bib):

        bib_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Citation</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
            <div style="overflow-x: auto; background-color: whitesmoke; color: black;">
                {hilite_me.bib_formatter(bib)}
            </div>
	    </div>"""

        ro_html.append_component(self.soup, "bibtext", bib_component)
        ro_html.sidebar_append(self.soup, "bibtext", "Bibtext")

    def init_help_page(self):


        logo_recognition_explained_component = ""

        if self.worth:

            if self.data.type == "paper":
                logo_recognition_explained =f"""
                <p>This icon showcases that this paper meets all the following requirements, so it is considered to be a complete Paper:</p>
                {self.ul_component([ req.replace("_", " ").capitalize() for req in self.data.requirements ])}
                """                
                img_component =f"""
                <img title="This paper has the necessary characteristics to be recognized as an complete paper."
					alt="Complete-Paper" src="images/complete_paper.png" style="width: 8em;"/>
                """
                
                logo_recognition_explained_component = ro_html.html_horizontal(img_component, logo_recognition_explained)

            if self.data.type == "project":
                logo_recognition_explained =f"""
                <p>This EELISA logo showcases that this project meets all the following requirements, so it is considered to be a complete/eligible EELISA project:</p>
                {self.ul_component(req.replace("_", " ").capitalize() for req in self.data.requirements)}
                """
                img_component =f"""
                <img title="This project has the necessary characteristics to be recognized as an EELISA project."
					alt="EELISA-logo" src="https://eelisa.eu/wp-content/uploads/2020/11/logo-white-1.png" style="width: 3em; width: fit-content;"/>
                """
                logo_recognition_explained_component = ro_html.html_horizontal(img_component, logo_recognition_explained)

        help_button_exaplained = "It is a help button that redirects to this page, where you can find a more in-depth explanation of the website."

        jsonld_button_exaplained = "It is a button that redirects you to a JSON-LD RO-Crate representation of the data of this webpage, which is used to ease the understanding of the content to machines."

        icons_explanation_component = f"""
        <div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Icons</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
        """ + ro_html.html_horizontal(
            """<img title="Description of each element and how was this webpage created."
			alt="help-button" src="https://img.icons8.com/material-outlined/48/000000/help.png" 
			style="filter: invert(100%) sepia(100%) saturate(0%) hue-rotate(57deg) brightness(101%) contrast(102%);
            width: 60px; margin: 0; display:block; margin-left:auto; margin-right:auto;"/>""",
            f"""<p>{help_button_exaplained}</p>""") + f"""

        """ + ro_html.html_horizontal("""<img title="Retrieve the JSON-LD ro-crate representation of this webpage."
			alt="JSON-LD" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/JSON-LD.svg/512px-JSON-LD.svg.png" 
			style="filter: invert(100%) sepia(100%) saturate(0%) hue-rotate(57deg) brightness(101%) contrast(102%);
            width: 60px; margin: 0; display:block; margin-left:auto; margin-right:auto;"/>""",
            f"<p>{jsonld_button_exaplained}</p>") + f"""
    
        {logo_recognition_explained_component}

	    </div>
        """

        ro_html.append_component(self.soup_help, "icons_explanation", icons_explanation_component)

        ################################################

        how_info_text = f"""This webpage was created using the tool ya2ro which takes as an input a yaml file with all the relevant information and pointers to the webpage. Then, it merges the information retrieved from the webpage pointers with the provided information in the yaml file. In this case, the yaml file used was the following:"""

        with open(self.data.yaml_file, 'r') as f:
            yaml = f.read()

        how_info_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>How was the information retrieved?</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{how_info_text}</p>
            <div style="overflow-x: auto; background-color: whitesmoke; color: black;">
                {hilite_me.yaml_formatter(yaml)}
            </div>
	    </div>"""

        ro_html.append_component(self.soup_help, "how_info", how_info_component)


    def init_styles(self):

        if p.style == "dark":

            # TODO: Make a function out of this 
            style_component = """
            h1,h1 b{color:#fff!important}
            .w3-light-grey{background-color:#ddd!important;color:#222831!important}
            .w3-green{background-color:#30475e!important}.w3-round{border:5px solid #f05454!important}
            body{background-color:#222831!important;color:#fff!important}
            """
            ro_html.append_component(self.soup, "style", style_component)
            ro_html.append_component(self.soup_help, "style", style_component)
            

    def init_requirements_recognition(self, requirements):

        # LOGO WORTH IT?
        self.worth = True
        for req in requirements:
            val = getattr(self.data, req)
            if val is None:
                print("WARNING: '{}' is not defined. Add it to be eligible for beeing an EELISA project.".format(req))
                self.worth = False

        if self.worth and self.data.type == "project":

            elisa_logo_html = """<a href="https://eelisa.eu/" target="_blank" >
				<img title="This project has the necessary characteristics to be recognized as an EELISA project."
					alt="EELISA-logo" src="https://eelisa.eu/wp-content/uploads/2020/11/logo-white-1.png" style="width: 3em; width: fit-content;"/>
			</a>"""
            ro_html.append_component(self.soup, "recogn_logo", elisa_logo_html)

        if self.worth and self.data.type == "paper":

            # copy image to output/images directory
            src = Path("images","complete_paper.png")
            dst = Path(self.data.output_directory_datafolder, "images","complete_paper.png")
            copyfile(src, dst)

            complete_logo_html = """<a href="#">
				<img title="This paper has the necessary characteristics to be recognized as an complete paper."
					alt="Complete-Paper" src="images/complete_paper.png" style="width: 8em;"/>
			</a>"""
            ro_html.append_component(self.soup, "recogn_logo", complete_logo_html)
    
    def init_social_motivation(self, social_motivation):

        social_motivation_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Social Motivation</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{social_motivation}</p>
	    </div>"""

        ro_html.append_component(self.soup, "social_motivation", social_motivation_component)
        ro_html.sidebar_append(self.soup, "social_motivation", "Social motivation")
    

    def init_sketch(self, sketch):
        
        sketch_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Sketch</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<img src="{sketch}" alt="Sketch of the project" style="width: 100%;">
	    </div>"""

        ro_html.append_component(self.soup, "sketch", sketch_component)
        ro_html.sidebar_append(self.soup, "sketch", "Sketch")

        # copy image to output/images directory
        src = Path(sketch)
        dst = Path(self.data.output_directory_datafolder, sketch)
        copyfile(src, dst)
    

    def init_areas(self, areas):

        areas_list = self.ul_component(areas)

        areas_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Areas</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		{areas_list}
	    </div>"""

        ro_html.append_component(self.soup, "areas", areas_component)
        ro_html.sidebar_append(self.soup, "areas", "Areas")


    def init_contact(self, contact):

        contact_elements = []
        contact_elements.append(f"Email: {contact.email}")
        contact_elements.append(f"Phone: {contact.phone}")

        contact_list = self.ul_component(contact_elements)

        contact_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Contact</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		{contact_list}
	    </div>"""

        ro_html.append_component(self.soup, "contact", contact_component)
        ro_html.sidebar_append(self.soup, "contact", "Contact")
        

    def init_activities(self, activities):

        activities_list = self.ul_component(activities)

        activities_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Activities</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		{activities_list}
	    </div>"""

        ro_html.append_component(self.soup, "activities", activities_component)
        ro_html.sidebar_append(self.soup, "activities", "Activities")


    def init_demo(self, demo):

        demo_list_commponent = self.ul_component([f"""<a href="{d.link}">{d.link if d.name is None else d.name}</a>: {d.description}""" for d in demo])

        demo_component = f"""<div class="w3-container" id="demo" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Demo</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
        {demo_list_commponent}
	    </div>"""

        ro_html.append_component(self.soup, "demo", demo_component)
        ro_html.sidebar_append(self.soup, "demo", "Demo")


    def init_goal(self, goal):

        goal_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Goal</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{goal}</p>
	    </div>"""

        ro_html.append_component(self.soup, "goal", goal_component)
        ro_html.sidebar_append(self.soup, "goal", "Goal")
 

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

        ro_html.append_component(self.soup, "summary", summary_component)
        ro_html.sidebar_append(self.soup, "summary", "Summary")


    def init_datasets(self, datasets):

        def html_entry_datasets(d):
            dataset_attr = []
            if d.path:
                if d.description:
                    dataset_attr.append(f"<b>Description:</b> {d.description}")
                
                if d.license:
                    dataset_attr.append(f"<b>License:</b> {d.license}")
                
                if d.author:
                    dataset_attr.append(f"<b>Author:</b> {d.author}")
                
                if d.files:
                    dataset_attr.append("<p>Pointers to download datasets:</p>" +
                        self.ul_component([ f"""<a href="{ds}" download>{os.path.basename(Path(ds))}</a>""" for ds in d.files ])
                        )

                return f"""<p>{d.path if d.name is None else d.name}</p>
                {self.ul_component(dataset_attr)}"""
            else:
                if d.description:
                    dataset_attr.append(f"<b>Description:</b> {d.description}")
                
                if d.license:
                    dataset_attr.append(f"<b>License:</b> {d.license}")
                
                if d.author:
                    dataset_attr.append(f"<b>Author:</b> {d.author}")

                return f"""<p><a href="{d.link}">{d.link if d.name is None else d.name}</a></p>
                {self.ul_component(dataset_attr)}"""

        dataset_entries = [ html_entry_datasets(d) for d in datasets ]
        datasets_list_commponent = self.ul_component(dataset_entries)
 
        datasets_component = f"""<div class="w3-container" id="datasets" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Datasets</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
        {datasets_list_commponent}
	    </div>"""

        ro_html.sidebar_append(self.soup, "datasets", "Datasets")
        ro_html.append_component(self.soup, "datasets", datasets_component)
    

    def init_software(self, software):

        def html_entry_software(s):
            software_attr = []

            if s.description:
                software_attr.append(f"<b>Description:</b> {s.description}")
            
            if s.license:
                software_attr.append(f"<b>License:</b> {s.license}")

            return f"""<p><a href="{s.link}">{s.link if s.name is None else s.name}</a></p>
            {self.ul_component(software_attr)}"""

        software_cards_scc = ''
        software_cards_html = []
        
        for s in software:
            if s.metadata and not p.no_somef:
                software_cards_scc += card_html_view(s.metadata,embedded=True)
            else:
                software_cards_html.append(html_entry_software(s))

        software_cards_component = f"""
            {self.ul_component(software_cards_html)}
            <div style="max-width: 1600px;display: flex; align-content: flex-start; flex-wrap: wrap; 
            flex-direction: row;justify-content: center; margin-top: 3rem;">{software_cards_scc}</div>"""

        software_component = f"""<div class="w3-container" id="software" style="margin-top:75px">
        <h1 class="w3-xxxlarge w3-text-green"><b>Software</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
        The pointers for the main software used can be found below:
        {software_cards_component}
        </div>"""

        ro_html.sidebar_append(self.soup, "software", "Software")
        ro_html.append_component(self.soup, "software", software_component)
    

    def init_bibliography(self, bibliography):
        
        def html_activate_links(text):
            return re.sub(
                pattern=r'(http[^ 	)(]*)', 
                repl='<a href="\\1" target="_blank">\\1</a>', 
                string=text
            )
        bibliography_list = self.ul_component([html_activate_links(b.entry) for b in bibliography])

        bibliography_commponent = f"""<div class="w3-container" id="bib" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Bibliography</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
		{bibliography_list}
	    </div>"""

        ro_html.sidebar_append(self.soup, "bibliography", "Bibliography")
        ro_html.append_component(self.soup, "bibliography", bibliography_commponent)


    def init_authors(self, authors):
        # create authors
        authors_boxes = self.create_about_authors(authors)
        authors_commponent = f"""<div class="w3-container" id="authors" style="margin-top:75px">
        <h1 class="w3-xxxlarge w3-text-green"><b>About the authors</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
        {authors_boxes}"""

        ro_html.sidebar_append(self.soup, "authors", "About the authors")
        ro_html.append_component(self.soup, "authors", authors_commponent)

        # copy images to output/images directory
        for author in authors:

            src = str(author.photo)
            default_photo = str(Path(p.input_to_vocab["images"], p.properties["default_author_img"]))
            
            if src == default_photo:
                src = Path(p.base_dir, p.input_to_vocab["images"], p.properties["default_author_img"])
                
            dst = Path(self.data.output_directory_datafolder, author.photo)

            copyfile(src, dst)


    def create_about_authors(self, authors):

        num_authors = 0
        html_author = ""

        for author in authors:

            num_authors += 1

            if((num_authors-1) %3 == 0):
                html_author += """<div class="w3-row-padding">"""
            
            author_name_component = f"""<h3><a href="{author.orcid if author.orcid else author.web if author.web else ""}">{author.name}</a></h3>""" if author.name else ""
            author_role_component = f"""<p class="w3-opacity">{author.role}</p>""" if author.role else ""
            author_position_component = f"""<p class="w3-opacity">{author.position}</p>""" if author.position else ""
            author_web_component = f"""<a href="{author.web}">{author.web}</a>""" if author.web else ""
            author_description_component = f"""<p>{author.description}</p>""" if author.description else ""

            html_author += f"""
            <div class="w3-col m4 w3-margin-bottom">
                <div class="w3-light-grey" style="padding-bottom: 10px;">
                <div style="width:90%; height:0; overflow:hidden; height:0; padding-top: 12px; padding-bottom: 90%;
                            margin: auto;">
                    <img src="{author.photo}" alt="{author.name if author.name else ""}" style="width:100%;">
                </div>
                <div class="w3-container">
                    {author_name_component}
                    {author_role_component}
                    {author_position_component}
                    {author_web_component}
                    {author_description_component}
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
        with open(self.data.output_html, "w+") as file:
            file.write(str(self.soup))

        # dump changes into help.html
        with open(self.data.output_html_help, "w+") as file:
            file.write(str(self.soup_help))

        print(f"HTML website file created at {self.data.output_html}")   
        print(f"HTML help website file created at {self.data.output_html_help}")   


    def append_component(soup, location_id, str_component):
        loc = soup.find(id=location_id)
        html_component = BeautifulSoup(str_component, 'html.parser')
        loc.append(html_component)


    def sidebar_append(soup, location_id, item_name):
        item_component = f"""<a href="#{location_id}" onclick="w3_close()" class="w3-bar-item w3-button w3-hover-white">{item_name}</a>"""
        ro_html.append_component(soup, "sidebar", item_component)


    def ul_component(self, list):
        ul_list = """<ul>"""
        for li in list:
            ul_list += f"""<li>{li}</li>"""
        ul_list += """</ul>"""
        return ul_list
    
    
    def html_horizontal(left_element, rigth_element):
        return f"""	<div class="row" >
		<div class="column" style="width:30%;">
        {left_element}
		</div>
        <div class="column" style="width:70%;">
        {rigth_element}
		</div>
	    </div>"""


