import Properties as prop
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
            "name": prop.data[prop.input_to_vocab["title"]],
            "description": prop.data[prop.input_to_vocab["summary"]],
            "author": [],
            "hasPart": []
        }
        ]

        # Self creates the hardcoded structure
        self.graph_add_authors(prop.data[prop.input_to_vocab["authors"]], graph)
        self.graph_add_softwares(prop.data[prop.input_to_vocab["software"]], graph)
        self.graph_add_datasets(prop.data[prop.input_to_vocab["datasets"]][prop.input_to_vocab["datasets_links"]], graph)

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

            self._add_id_to_list(author[prop.input_to_vocab["name"]],
                                 graph[1]["author"])

            graph.append({
            "@id": self._normalize_name(author[prop.input_to_vocab["name"]]),
            "@type": "Person",
            "name": author[prop.input_to_vocab["name"]],
            "position": author[prop.input_to_vocab["position"]],
            "description": author[prop.input_to_vocab["description"]]
        })

    def graph_add_softwares(self, softwares, graph):

        for software in softwares:

            self._add_id_to_list(software[prop.input_to_vocab["name"]],
                                 graph[1]["hasPart"])

            graph.append({
            "@id": self._normalize_name(software[prop.input_to_vocab["name"]]),
            "installUrl": software[prop.input_to_vocab["link"]],
            "@type": "SoftwareApplication",
            "description": software[prop.input_to_vocab["description"]]
        })

    def graph_add_datasets(self, datasets, graph):
        
        for dataset in datasets:

            self._add_id_to_list(dataset[prop.input_to_vocab["name"]],
                                 graph[1]["hasPart"])

            graph.append({
                "@id": self._normalize_name(dataset[prop.input_to_vocab["name"]]),
                "@type": "Dataset",
                "name": dataset[prop.input_to_vocab["name"]],
                "description": dataset[prop.input_to_vocab["description"]],
                "distribution": {"@id": dataset[prop.input_to_vocab["link"]]}
            })

            graph.append({
                "@id": dataset[prop.input_to_vocab["link"]],
                "@type": "DataDownload",
                "encodingFormat": "application/zip"
            })

    def createJSONLD_file(self):
        # dump changes into output/ro-crate.json
        with open(prop.properties["output_jsonld"], "w+") as file:
            file.write(json.dumps(self.jsonld, indent=4, sort_keys=True))

