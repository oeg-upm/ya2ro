import properties as p
import json
import data_wrapper


class ro_jsonld(object):

    def __init__(self):

        self.jsonld = {}
        self.jsonld["@context"] = "https://w3id.org/ro/crate/1.1/context"
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
                "@type": "Dataset",
                "name": p.data.title,
                "description": "",
                "author": [],
                "hasPart": []
            }
        ]

        # Self creates the hardcoded structure for paper
        if isinstance(p.data, data_wrapper.Paper):
            self.graph_add_description(p.data.summary, graph)
            self.graph_add_authors(p.data.authors, graph)
            self.graph_add_softwares(p.data.software, graph)
            self.graph_add_datasets(p.data.datasets, graph)
        
        # Self creates the hardcoded structure for project
        if isinstance(p.data, data_wrapper.Project):
            self.graph_add_description(p.data.goal, graph)
            self.graph_add_authors(p.data.authors, graph)
            self.graph_add_softwares(p.data.software, graph)
            self.graph_add_datasets(p.data.datasets, graph)

        # Adds graph to the final structure jsonld
        self.jsonld["@graph"] = graph

    def _normalize_name(self, name):
        """Normalizes names in order to be used as an ID."""
        return "#" + str(name).replace(' ', '_').lower()

    def _add_id_to_list(self, name, list):
        """Enters a name with blank spaces or not and appends
        to the list a id normalized version of the name. List 
        must be a list of dicts."""

        id_normalized = self._normalize_name(name)
        list.append({
            "@id": id_normalized
        })

    def graph_add_description(self, summary, graph):
        
        if summary is None:
            return

        graph[1]["description"] = summary

    def graph_add_authors(self, authors, graph):

        if authors is None:
            return

        for author in authors:

            self._add_id_to_list(author.name, graph[1]["author"])

            graph.append({
            "@id": self._normalize_name(author.name),
            "@type": "Person",
            "name": author.name,
            "position": author.position.split(", "),
            "description": author.description
        })

    def graph_add_softwares(self, softwares, graph):

        if softwares is None:
            return

        for software in softwares:

            self._add_id_to_list(software.name, graph[1]["hasPart"])

            graph.append({
            "@id": self._normalize_name(software.name),
            "installUrl": software.link,
            "@type": "SoftwareApplication",
            "description": software.description
        })

    def graph_add_datasets(self, datasets, graph):

        if datasets is None:
            return
        
        for dataset in datasets:

            self._add_id_to_list(dataset.name, graph[1]["hasPart"])

            graph.append({
                "@id": self._normalize_name(dataset.name),
                "@type": "Dataset",
                "name": dataset.name,
                "description": dataset.description,
                "distribution": {"@id": dataset.link}
            })

    def createJSONLD_file(self):
        # dump changes into output/ro-crate.json
        with open(p.properties["output_jsonld"], "w+") as file:
            file.write(json.dumps(self.jsonld, indent=4, sort_keys=True))
        print(f"JSON-LD file created at {p.properties['output_jsonld']}")
        

