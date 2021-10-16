import Properties as p
import json

class Ro_jsonld(object):

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
            "name": p.paper.title,
            "description": p.paper.summary,
            "author": [],
            "hasPart": []
        }
        ]

        # Self creates the hardcoded structure
        self.graph_add_authors(p.paper.authors, graph)
        self.graph_add_softwares(p.paper.software, graph)
        self.graph_add_datasets(p.paper.datasets, graph)

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

    def graph_add_authors(self, authors, graph):

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

        for software in softwares:

            self._add_id_to_list(software.name, graph[1]["hasPart"])

            graph.append({
            "@id": self._normalize_name(software.name),
            "installUrl": software.link,
            "@type": "SoftwareApplication",
            "description": software.description
        })

    def graph_add_datasets(self, datasets, graph):
        
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
        

