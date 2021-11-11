import os
import properties as p
from bs4 import BeautifulSoup
import data_wrapper
from pathlib import Path
from ro_html import ro_html

class ro_landing_page(object):

    def __init__(self, landing_page_directory):

        if not Path(landing_page_directory).is_dir():
            print("Error: '-l','--landing_page' argument incorrect. Directory does not exist or is a file.")
            exit()
        
        self.list_data = []

        for data_folder in os.scandir(landing_page_directory):
            if data_folder.is_dir():
                for entry in os.scandir(data_folder):
                    if entry.path.endswith(".json") and entry.is_file():
                        print("Parsing JSON-LD: " + str(Path(entry)))
                        data = data_wrapper.load_jsonld(entry)
                        data.index_html = Path(Path(data_folder).stem ,data.index_html)
                        self.list_data.append(data)


    def create_landing_page(self):

        soup_landing = BeautifulSoup(open(p.properties["template_landing"]), 'html.parser')

        # Apply css style
        if p.style == "dark":
            style_component = """
                h1,h1 b{color:#fff!important}
                .w3-light-grey{background-color:#ddd!important;color:#222831!important}
                .w3-green{background-color:#30475e!important}.w3-round{border:5px solid #f05454!important}
                body{background-color:#222831!important;color:#fff!important}
                """
            ro_html.append_component(soup_landing, "style", style_component)

        abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for letter in abc:
            item_component = f"""
            <a href="#{letter}" 
            onclick="w3_close()" 
            style ="padding:0; padding-left:16px; font-size:13px;"
            class="w3-bar-item w3-button w3-hover-white">{letter}</a>"""
            ro_html.append_component(soup_landing, "sidebar", item_component)

        def byTitle(elem):
            return elem.title
        
        self.list_data.sort(key=byTitle)
        for data in self.list_data:

            if data.type == "paper":
                description = data.summary
                
            if data.type == "project":
                description = data.goal

            id_component = data.title[:1].capitalize()

            web_entry_component = f"""<div class="w3-container" style="margin-top:15px" id="{id_component}">
            <a href="{data.index_html}"><h2><b>{data.title} ({str(data.type).capitalize()})</b></h2></a>
            <hr style="width:50px;border:5px solid green" class="w3-round">
            <details>
                    <summary class="w3-opacity">{description[:100]}...</summary>
                    <p>{description}</p>
            </details>
            </div>"""

            ro_html.append_component(soup_landing, "content", web_entry_component)
        
        # dump changes into output_html_landing
        with open(Path(p.output_directory, p.properties["output_html_landing"]), "w+") as file:
            file.write(str(soup_landing))

        # Create htaccess for landing page
        import htaccess
        htaccess.create_htaccess_landing(p.output_directory)

        print(f"""Landing page created at {p.output_directory}/{p.properties["output_html_landing"]} \n""")