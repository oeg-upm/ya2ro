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
            "@type": "Paper",
            "name": prop.data[prop.input_to_vocab["title"]],
            "description": prop.data[prop.input_to_vocab["summary"]],
            "author": [],
            "hasPart": [
                {"@id": "#softwares"},
                {"@id": "#datasets"}
            ]
        }
        ]

        self.graph_add_authors(prop.data[prop.input_to_vocab["authors"]], graph)
        self.graph_add_softwares(prop.data[prop.input_to_vocab["software"]], graph)
        self.graph_add_datasets(prop.data[prop.input_to_vocab["datasets"]], graph)

        self.jsonld["@graph"] = graph

    def graph_add_authors(self, authors, graph):

        graph[1]["author"] = []

        for author in authors:

            graph[1]["author"].append(author[prop.input_to_vocab["name"]])

            graph.append({
            "@id": "#"+author[prop.input_to_vocab["name"]],
            "@type": "Person",
            "name": author[prop.input_to_vocab["name"]],
            "position": author[prop.input_to_vocab["position"]],
            "description": author[prop.input_to_vocab["description"]]
        })

    def graph_add_softwares(self, softwares, graph):

        software_node = {
            "@id": "#softwares",
            "@type": "SoftwareApplication",
            "hasPart": []
        }
        
        for software in softwares:

            software_node["hasPart"].append(software[prop.input_to_vocab["name"]])

            graph.append({
            "@id": software[prop.input_to_vocab["name"]],
            "installUrl": software[prop.input_to_vocab["link"]],
            "@type": "SoftwareApplication",
            "description": software[prop.input_to_vocab["description"]]
        })

        graph.insert(-len(softwares),software_node)

    def graph_add_datasets(self, datasets, graph):

        dataset_node = {
            "@id": "#datasets",
            "@type": "Dataset",
            "hasPart": []
        }
        
        for dataset in datasets:
            dataset_node["hasPart"].append(dataset[prop.input_to_vocab["name"]])

            graph.append({
                "@id": dataset[prop.input_to_vocab["name"]],
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

        graph.insert(-len(datasets)*2, dataset_node)

    def createJSONLD_file(self):
        # dump changes into self.jsonld
        with open(prop.properties["output_jsonld"], "w") as file:
            file.write(json.dumps(self.jsonld, indent=4, sort_keys=True))

