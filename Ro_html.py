import properties as p
from bs4 import BeautifulSoup
from shutil import copyfile
from pathlib import Path
import ntpath

class ro_html(object):

    def __init__(self):

        # read and parse the templates
        self.soup = BeautifulSoup(open(p.properties["template_html"]), 'html.parser')
        self.soup_help = BeautifulSoup(open(p.properties["template_help"]), 'html.parser')

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
            "demo": self.init_demo,
            "requirements": self.init_requirements_recognition

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

    def init_help_page(self):

        icons_explanation_text = "Icons description: [...]"

        icons_explanation_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Icons</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{icons_explanation_text}</p>
	    </div>"""

        ro_html.__append_component(self.soup_help, "icons_explanation", icons_explanation_component)

        ################################################

        how_info_text = "How information was retrieved: [...]"

        how_info_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>How was the information retrieved?</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{how_info_text}</p>
	    </div>"""

        ro_html.__append_component(self.soup_help, "how_info", how_info_component)


    def init_styles(self):

        if p.style == "dark":

            # TODO: Make a function out of this 
            style_component = """
            h1,h1 b{color:#fff!important}
            .w3-light-grey{background-color:#ddd!important;color:#222831!important}
            .w3-green{background-color:#30475e!important}.w3-round{border:5px solid #f05454!important}
            body{background-color:#222831!important;color:#fff!important}
            """
            ro_html.__append_component(self.soup, "style", style_component)
            ro_html.__append_component(self.soup_help, "style", style_component)
            

    def init_requirements_recognition(self, requirements):

        # LOGO WORTH IT?
        worth = True
        for req in requirements:
            val = getattr(self.data, req)
            if val is None:
                print("WARNING: '{}' is not defined. Add it to be eligible for beeing an EELISA project.".format(req))
                worth = False

        if worth and self.data.type == "project":

            elisa_logo_html = """<a href="https://eelisa.eu/" target="_blank" >
				<img title="This project has the necessary characteristics to be recognized as an EELISA project."
					alt="EELISA-logo" src="https://eelisa.eu/wp-content/uploads/2020/11/logo-white-1.png" style="width: 3em; width: fit-content;"/>
			</a>"""
            ro_html.__append_component(self.soup, "recogn_logo", elisa_logo_html)

        if worth and self.data.type == "paper":

            # copy image to output/images directory
            src = Path("images","complete_paper.png")
            dst = Path(self.data.output_directory_datafolder, "images","complete_paper.png")
            copyfile(src, dst)

            complete_logo_html = """<a href="#">
				<img title="This paper has the necessary characteristics to be recognized as an complete paper."
					alt="Complete-Paper" src="images/complete_paper.png" style="width: 8em;"/>
			</a>"""
            ro_html.__append_component(self.soup, "recogn_logo", complete_logo_html)
    
    def init_social_motivation(self, social_motivation):

        social_motivation_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Social Motivation</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{social_motivation}</p>
	    </div>"""

        ro_html.__append_component(self.soup, "social_motivation", social_motivation_component)
        ro_html.__sidebar_append(self.soup, "social_motivation", "Social motivation")
    

    def init_sketch(self, sketch):
        
        sketch_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Sketch</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<img src="{sketch}" alt="Sketch of the project">
	    </div>"""

        ro_html.__append_component(self.soup, "sketch", sketch_component)
        ro_html.__sidebar_append(self.soup, "sketch", "Sketch")

        # copy image to output/images directory
        src = Path(sketch)
        dst = Path(self.data.output_directory_datafolder, sketch)
        copyfile(src, dst)
    

    def init_areas(self, areas):

        areas_list = self.__ul_component(areas)

        areas_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Areas</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		{areas_list}
	    </div>"""

        ro_html.__append_component(self.soup, "areas", areas_component)
        ro_html.__sidebar_append(self.soup, "areas", "Areas")


    def init_demo(self, demo):

        demo_list_commponent = self.__ul_component([f"""<a href="{d.link}">{d.link if d.name is None else d.name}</a>: {d.description}""" for d in demo])

        demo_component = f"""<div class="w3-container" id="software" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Demo</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
        {demo_list_commponent}
	    </div>"""

        ro_html.__append_component(self.soup, "demo", demo_component)
        ro_html.__sidebar_append(self.soup, "demo", "Demo")


    def init_goal(self, goal):

        goal_component = f"""<div class="w3-container" style="margin-top:15px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Goal</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
		<p>{goal}</p>
	    </div>"""

        ro_html.__append_component(self.soup, "goal", goal_component)
        ro_html.__sidebar_append(self.soup, "goal", "Goal")
 

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

        ro_html.__append_component(self.soup, "summary", summary_component)
        ro_html.__sidebar_append(self.soup, "summary", "Summary")

    def init_datasets(self, datasets):
 
        datasets_list_commponent = self.__ul_component([f"""<a href="{d.link}">{d.link if d.name is None else d.name}</a>: {d.description}""" for d in datasets])

        doi_datasets = ""
        if self.data.doi_datasets is not None:
            doi_datasets = f"""We used the following datasets for our data, available in Zenodo under DOI: <a href="{self.data.doi_datasets}">{self.data.doi_datasets}</a>"""
        
        datasets_component = f"""<div class="w3-container" id="software" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Datasets</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
        {doi_datasets}
        {datasets_list_commponent}
	    </div>"""

        ro_html.__sidebar_append(self.soup, "datasets", "Datasets")
        ro_html.__append_component(self.soup, "datasets", datasets_component)
    

    def init_software(self, software):

        software_list_commponent = self.__ul_component([f"""<a href="{s.link}">{s.link if s.name is None else s.name}</a>: {s.description}""" for s in software])

        software_component = f"""<div class="w3-container" id="software" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Software</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
        The pointers for the main software used can be found below:
        {software_list_commponent}
	    </div>"""

        ro_html.__sidebar_append(self.soup, "software", "Software")
        ro_html.__append_component(self.soup, "software", software_component)
    

    def init_bibliography(self, bibliography):
 
        bibliography_list = self.__ul_component([b.entry for b in bibliography])

        bibliography_commponent = f"""<div class="w3-container" id="bib" style="margin-top:75px">
		<h1 class="w3-xxxlarge w3-text-green"><b>Bibliography</b></h1>
		<hr style="width:50px;border:5px solid green" class="w3-round">
		{bibliography_list}
	    </div>"""

        ro_html.__sidebar_append(self.soup, "bibliography", "Bibliography")
        ro_html.__append_component(self.soup, "bibliography", bibliography_commponent)


    def init_authors(self, authors):
        # create authors
        authors_boxes = self.__create_about_authors(authors)
        authors_commponent = f"""<div class="w3-container" id="authors" style="margin-top:75px">
        <h1 class="w3-xxxlarge w3-text-green"><b>About the authors</b></h1>
        <hr style="width:50px;border:5px solid green" class="w3-round">
        {authors_boxes}"""

        ro_html.__sidebar_append(self.soup, "authors", "About the authors")
        ro_html.__append_component(self.soup, "authors", authors_commponent)

        # copy images to output/images directory
        for author in authors:

            src = Path(author.photo)
            dst = Path(self.data.output_directory_datafolder, author.photo)
            
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
                    <p class="w3-opacity">{author.role}</p>
                    <p class="w3-opacity">{author.position}</p>
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
        with open(self.data.output_html, "w+") as file:
            file.write(str(self.soup))

        # dump changes into help.html
        with open(self.data.output_html_help, "w+") as file:
            file.write(str(self.soup_help))

        print(f"HTML website file created at {self.data.output_html}")   
        print(f"HTML help website file created at {self.data.output_html_help}")   



    def __append_component(soup, location_id, str_component):
        loc = soup.find(id=location_id)
        html_component = BeautifulSoup(str_component, 'html.parser')
        loc.append(html_component)


    def __sidebar_append(soup, location_id, item_name):
        item_component = f"""<a href="#{location_id}" onclick="w3_close()" class="w3-bar-item w3-button w3-hover-white">{item_name}</a>"""
        ro_html.__append_component(soup, "sidebar", item_component)


    def __ul_component(self, list):
        ul_list = """<ul>"""
        for li in list:
            ul_list += f"""<li>{li}</li>"""
        ul_list += """</ul>"""
        return ul_list
    
    def create_landing_page(list_data):

        soup_landing = BeautifulSoup(open(p.properties["template_landing"]), 'html.parser')

        # Apply css style
        if p.style == "dark":
            style_component = """
                h1,h1 b{color:#fff!important}
                .w3-light-grey{background-color:#ddd!important;color:#222831!important}
                .w3-green{background-color:#30475e!important}.w3-round{border:5px solid #f05454!important}
                body{background-color:#222831!important;color:#fff!important}
                """
            ro_html.__append_component(soup_landing, "style", style_component)

        for data in list_data:

            if data.type == "paper":
                description = data.summary
            if data.type == "project":
                description = data.goal

            id_component = data.title.replace(" ", "_")
            # Remove first folder from path: "output" folder is deleted
            datafolder_indexhtml = str(Path(*data.output_html.parts[1:]))

            web_entry_component = f"""<div class="w3-container" style="margin-top:15px" id="{id_component}">
            <a href="{datafolder_indexhtml}"><h1 class="w3-text-green"><b>{data.title}</b></h1></a>
            <p><b>Type: {data.type.capitalize()}</b></p>
            <hr style="width:50px;border:5px solid green" class="w3-round">
            <p>{description}</p>
            </div>"""

            ro_html.__append_component(soup_landing, "content", web_entry_component)
            ro_html.__sidebar_append(soup_landing, id_component, data.title)
        
        # dump changes into output_html_landing
        with open(Path(p.output_directory, p.properties["output_html_landing"]), "w+") as file:
            file.write(str(soup_landing))

        # Create htaccess for landing page
        import htaccess
        htaccess.create_htaccess_landing(p.output_directory)

        print(f"""Landing page created at {p.output_directory}/{p.properties["output_html_landing"]} \n""")
            

            


            

