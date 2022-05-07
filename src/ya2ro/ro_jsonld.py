from pandas import notnull
from . import properties as p
import json

class ro_jsonld(object):

    def __init__(self):

        self.jsonld = {}
        self.jsonld["@context"] = "https://w3id.org/ro/crate/1.1/context"
        self.graph = [
            {
                "@type": "CreativeWork",
                "@id": "ro-crate-metadata.json",
                "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
                "about": {"@id": "./"},
                "description": "RO-Crate Metadata File Descriptor (this file)"
            },
            {
                "@id": "./",
                "@type": "Dataset",
                "name": "",
                "DataType": "",
                "description": "",
                "author": [],
                "hasPart": []
            }
        ]


    def load_data(self, data):

        self.data = data
        self.graph_add_title(self.data.title)

        # Self creates the hardcoded structure for paper
        if self.data.type == "paper":
            self.graph_add_data_type(self.data.type)
            self.graph_add_description(self.data.summary)
            self.graph_add_authors(self.data.authors)
            self.graph_add_software(self.data.software)
            self.graph_add_datasets(self.data.datasets)
            self.graph_add_html_ref(p.properties["output_html"])
        
        # Self creates the hardcoded structure for project
        if self.data.type == "project":
            self.graph_add_data_type(self.data.type)
            self.graph_add_description(self.data.goal)
            self.graph_add_authors(self.data.authors)
            self.graph_add_software(self.data.software)
            self.graph_add_datasets(self.data.datasets)
            self.graph_add_demo(self.data.demo)
            self.graph_add_html_ref(p.properties["output_html"])


        # Adds graph to the final structure jsonld
        self.jsonld["@graph"] = self.graph

    def graph_add_html_ref(self, html_ref):

        if html_ref is None:
            return None

        self.graph[1]["hasPart"].append({
            "@id": html_ref
        })

        self.graph.append({ 
            "@id": html_ref, 
            "name": "HTML representation of this data.", 
            "@type": "WebPage"
            })
        

    def graph_add_data_type(self, type):

        if type is None:
            return None
        
        self.graph[1]["DataType"] = str(type).capitalize()
    

    def graph_add_title(self, title):

        if title is None:
            return None
        
        self.graph[1]["name"] = title

    def graph_add_demo(self, demo):

        if demo is None:
            return None

        workExample_list = []
        for d in demo:
            workExample_list.append(
                {
                    "@type": "Demo",
                    "link": d.link,
                    "name": d.name,
                    "description": d.description

                })
        self.graph.append({ "workExample": workExample_list })
            


    def graph_add_description(self, description):

        if description is None:
            return

        self.graph[1]["description"] = description


    def graph_add_authors(self, authors):

        if authors is None:
            return

        for author in authors:
            id = self._normalize_name(author.name) if not author.orcid else author.orcid
            self._add_id_to_list(id, self.graph[1]["author"], normalize=False)

            if author.position:
                position = author.position.split(", ")
            else:
                position = None

            self.graph.append({
                "@id": id,
                "@type": "Person",
                "name": author.name,
                "position": position,
                "description": author.description
        })

    def graph_add_software(self, softwares):

        if softwares is None:
            return

        for software in softwares:

            self._add_id_to_list(software.name, self.graph[1]["hasPart"])

            self.graph.append({
            "@id": self._normalize_name(software.name),
            "installUrl": software.link,
            "@type": "SoftwareApplication",
            "description": software.description
        })


    def graph_add_datasets(self, datasets):

        if datasets is None:
            return
        
        for dataset in datasets:

            self._add_id_to_list(dataset.name, self.graph[1]["hasPart"])

            self.graph.append({
                "@id": self._normalize_name(dataset.name),
                "@type": "Dataset",
                "name": dataset.name,
                "description": dataset.description,
                "distribution": {"@id": dataset.link}
            })


    def create_JSONLD_file(self):
        # dump changes into output/ro-crate.json
        self.jsonld = clean_nones(self.jsonld)
        with open(self.data.output_jsonld, "w+") as file:
            file.write(json.dumps(self.jsonld, indent=4, sort_keys=True))
        print(f"JSON-LD file created at {self.data.output_jsonld}")
        

    def _normalize_name(self, name):
        """
        Normalizes names in order to be used as an ID.
        """
        return "#" + str(name).replace(' ', '_').lower()


    def _add_id_to_list(self, name, list, normalize = True):
        """
        Enters a name with blank spaces or not and appends
        to the list a id normalized version of the name. List 
        must be a list of dicts.
        """

        list.append({
            "@id": self._normalize_name(name) if normalize else name
        })

def clean_nones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: clean_nones(val)
            for key, val in value.items()
            if val is not None
        }
    else:
        return value
